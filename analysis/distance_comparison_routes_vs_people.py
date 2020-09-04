import pandas as pd
from tqdm import tqdm
from pdb import set_trace as st
import os

"""
  Compares the distances of each person according to the output obtained from 0_people5to12.csv
  and the sum of the edges obtained from 0_route5to12.csv and edges.csv

  Args:
    edges_file: Path to the edges information file.

    people_file: Path to the people information file. Default: "../0_people5to12.csv"

    route_file: Path to the route information file. Default: "../0_route5to12.csv"

    stop_if_discrepancy_found:  if true, stops as soon as it finds a discrepancy between
                                the two distances of a person. Useful for testing without having to
                                wait for the whole network to be processed. Default: true

    output_file: Path to distance merge output. Default: distance_merge.csv
                Outputted as csv with 3 columns: person_id,distance_sum_of_edges,distance_people_info
  
  Returns:
    Nothing
"""
def merge_and_compare_route_vs_people_distances(
      edges_file,
      people_file = "../0_people5to12.csv",
      route_file = "../0_route5to12.csv",
      stop_if_discrepancy_found=True,
      output_file="distance_merge.csv"):
  
  if (os.path.isfile(output_file)):
    answer = "no answer yet"
    while(not answer.lower() in {"y","yes","n","no",""}):
      answer = raw_input("{} already exists. Do you want to replace it? (Y/n): ".format(output_file))
    if (answer.lower() in {"n","no"}):
      print("Stopping.")
      return

  print("Loading edges from {}...".format(edges_file))
  print("Loading people from {}...".format(people_file))
  print("Loading routes from {}...".format(route_file))
  pd_people = pd.read_csv(people_file)
  number_of_people = len(pd_people.index)
  pd_edges = pd.read_csv(edges_file)

  f = open(output_file, "w")
  f.write("person_id,distance_sum_of_edges,distance_people_info\n")

  print("Processing routes...")
  # reads in chunks of 1000 to reduce memory usage
  for chunk_route in tqdm(pd.read_csv(route_file, sep=":", chunksize=1000), total=number_of_people/1000):
    for _, row in chunk_route.iterrows():
      person_id = str(row["p"])
      route = str(row["route"])

      # gets each edge of the route inside the brackets
      route = route.replace("[", "").replace("]", "")
      route = route.split(",")  # split
      route = route[:-1]  # delete last element due to the extra comma

      # sums up the edges distances
      distance_sum_of_edges = 0
      for edge_id in route:
        distance_sum_of_edges += pd_edges.loc[int(edge_id)]["length"]

      distance_people_info = pd_people.loc[int(person_id)]['distance']

      f.write("{},{},{}\n".format(
        person_id, distance_sum_of_edges, distance_people_info))


      if (stop_if_discrepancy_found and distance_sum_of_edges != distance_people_info):
        print("Discrepancy has been found for person {}. \
              Distance according to people info: {}. \
              Distance according to sum of edges: {}. Stopping.". \
              format(person_id,distance_people_info,distance_sum_of_edges))
        return


  print("Saved {}.".format(output_file))
  f.close()

if __name__ == '__main__':
  merge_and_compare_route_vs_people_distances(
    "../LivingCity/berkeley_2018/new_full_network/edges.csv",
    people_file="../../0_people5to12.csv",
    route_file="../../0_route5to12.csv",
    stop_if_discrepancy_found=True,
    output_file="distances.csv")