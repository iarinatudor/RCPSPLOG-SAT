import pandas as pd
import matplotlib.pyplot as plt
import os


if __name__ == '__main__':
    # Define the base directory path
    base_dir = 'results\j30-VSIDS\BI1'

    # Create an empty DataFrame to store the combined data
    combined_df = pd.DataFrame()

    # Iterate over the directory names
    for dir_name in os.listdir(base_dir):
        # Construct the full directory path
        dir_path = os.path.join(base_dir, dir_name)
        # Check if the directory is valid and contains the file
        if os.path.isdir(dir_path) and os.path.exists(os.path.join(dir_path, 'run.log')):
            # Construct the file path
            file_path = os.path.join(dir_path, 'run.log')
            # Filter the DataFrame to rows starting with 'o'
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line.startswith('o'):
                        break
                    else:
                        _, second, third = line.split()
                        third = round(int(third) / 1e9)
                        combined_df = combined_df.append({'Second': int(second), 'Third': third},
                                                         ignore_index=True)

    # Calculate the average of value 2 at each unique third value
    avg_df = combined_df.groupby('Third')['Second'].mean().reset_index()

    # Define the base directory path
    base_dir = 'results\j30-makespan\BI1'

    # Create an empty DataFrame to store the combined data
    combined_df = pd.DataFrame()

    # Iterate over the directory names
    for dir_name in os.listdir(base_dir):
        # Construct the full directory path
        dir_path = os.path.join(base_dir, dir_name)
        # Check if the directory is valid and contains the file
        if os.path.isdir(dir_path) and os.path.exists(os.path.join(dir_path, 'run.log')):
            # Construct the file path
            file_path = os.path.join(dir_path, 'run.log')
            # Filter the DataFrame to rows starting with 'o'
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line.startswith('o'):
                        break
                    else:
                        _, second, third = line.split()
                        third = round(int(third) / 1e9)
                        combined_df = combined_df.append({'Second': int(second), 'Third': third},
                                                         ignore_index=True)

    # Calculate the average of value 2 at each unique third value
    avg_df2 = combined_df.groupby('Third')['Second'].mean().reset_index()



    # Define the base directory path
    base_dir = 'results\j30-heur\BI1'

    # Create an empty DataFrame to store the combined data
    combined_df = pd.DataFrame()

    # Iterate over the directory names
    for dir_name in os.listdir(base_dir):
        # Construct the full directory path
        dir_path = os.path.join(base_dir, dir_name)
        # Check if the directory is valid and contains the file
        if os.path.isdir(dir_path) and os.path.exists(os.path.join(dir_path, 'run.log')):
            # Construct the file path
            file_path = os.path.join(dir_path, 'run.log')
            # Filter the DataFrame to rows starting with 'o'
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line.startswith('o'):
                        break
                    else:
                        _, second, third = line.split()
                        third = round(int(third) / 1e9)
                        combined_df = combined_df.append({'Second': int(second), 'Third': third},
                                                         ignore_index=True)

    # Calculate the average of value 2 at each unique third value
    avg_df3 = combined_df.groupby('Third')['Second'].mean().reset_index()

    # Plot the average values
    plt.plot(avg_df2['Third'], avg_df2['Second'], label='Benchmark')
    plt.plot(avg_df['Third'], avg_df['Second'], label='EST + VSIDS')
    plt.plot(avg_df3['Third'], avg_df3['Second'], label='EST')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Average makespan')
    plt.title('Average of best makespan over time for 100% BI constraints')

    plt.legend()
    plt.show()


