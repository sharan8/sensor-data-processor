import sys
import os
import numpy as np
import matplotlib.pyplot as plt

MY_TIME_IDX = 3
SENDER_IDX = 5
SEQ_NO_IDX = 7
TIMESTAMP_IDX = 9

def plot_graph(reception_intervals):
  # get histogram data
  count, bins_count = np.histogram(reception_intervals, bins=10)
    
  # find pdf and cdf
  pdf = count / sum(count)
  cdf = np.cumsum(pdf)
    
  # plot pdf and cdf
  plt.plot(bins_count[1:], pdf, color="red", label="PDF")
  plt.plot(bins_count[1:], cdf, label="CDF")
  plt.legend()
  plt.title(raw_file)
  plt.xlabel("Interval (s)")
  plt.ylabel("Probability")
  plt.show()

# meta-level variables
all_first_reception_times = []
all_first_seq_numbers = []

for raw_file in os.listdir('./raw_output/'):
  reception_intervals = []
  prev_reception = -1
  first_reception = -1
  first_seq_no = -1
  packets_received = 0

  # read contents of file
  with open(f'./raw_output/{raw_file}') as f:
    lines = f.readlines()
    for line in lines:
      # remove commas
      line = line.replace(',', '')

      # create tokens
      tokens = line.split(" ")

      # remove empty strings used as placeholders
      tokens = list(filter(lambda x: x != '', tokens))

      # get values
      my_time = float(tokens[MY_TIME_IDX])
      seq_no = tokens[SEQ_NO_IDX]
      packets_received += 1

      # handle first reception
      if prev_reception == -1:
        prev_reception = first_reception = my_time
        first_seq_no = seq_no
        continue

      # handle subsequent receptions
      new_interval = my_time - prev_reception
      prev_reception = my_time
      reception_intervals.append(new_interval)
    
  # write summary output to a file
  print(first_reception)
  summary = open(f"summary_{raw_file}.txt", "x")

  # write total packets received
  summary.write("Packets Received: ")
  summary.write(str(packets_received))
  summary.write('\n')
  
  # write first reception
  summary.write("First Reception: ")
  summary.write(str(first_reception))
  summary.write('\n')

  # first seq no
  summary.write("First Seq. No. Received: ")
  summary.write(first_seq_no)
  summary.write('\n')

  # write average interval
  summary.write("Average Interval: ")
  summary.write(str(sum(reception_intervals)/len(reception_intervals)))
  summary.write('\n')

  # write intervals
  summary.write('\n')
  summary.write("Intervals:")
  summary.write('\n')
  for interval in reception_intervals:
    summary.write(str(interval))
    summary.write('\n')

  all_first_seq_numbers.append(int(first_seq_no))
  all_first_reception_times.append(float(first_reception))

  # plot a graph based on data in this file
  plot_graph(reception_intervals)

  summary.close()

# write meta-stats to new file
overall_summary = open(f"overall_summary.txt", "x")

# write average first packet seq no.
overall_summary.write("Average First Packet Seq. No. Received: ")
overall_summary.write(str(sum(all_first_seq_numbers)/len(all_first_seq_numbers)))
overall_summary.write('\n')

# write average first reception time
overall_summary.write("Average Interval: ")
overall_summary.write(str(sum(all_first_reception_times)/len(all_first_reception_times)))
overall_summary.write('\n')

overall_summary.close()
