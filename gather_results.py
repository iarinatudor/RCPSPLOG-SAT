import os
import pandas as pd


if __name__ == '__main__':
    def process_csv_file(file_path):
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Calculate the average of the first and second columns
        print(df['number_of_decisions'])
        avg_decisions = int(df['number_of_decisions'].mean())
        avg_solve_time = df['solve_time'].mean()

        # Count the occurrences of "OPTIMAL" and "UNKNOWN" in the status column
        count_optimal = df[df['status'] == 'OPTIMAL'].shape[0]
        count_unknown = df[df['status'] == 'UNKNOWN'].shape[0]

        return avg_decisions, avg_solve_time, count_optimal, count_unknown


    def process_directory(directory_path):
        # Get a list of all files in the directory
        files = os.listdir(directory_path)

        # Create an empty DataFrame to store the results
        results_df = pd.DataFrame(columns=['File', 'Avg Decisions', 'Avg Solve Time', 'OPTIMAL Count', 'UNKNOWN Count'])

        # Process each file
        for file in files:
            file_path = os.path.join(directory_path, file)

            # If the file is a CSV file, process it
            if file.endswith('.csv'):
                avg_decisions, avg_solve_time, count_optimal, count_unknown = process_csv_file(file_path)

                # Append the results to the DataFrame
                results_df = results_df.append({'File': file_path.split('\\')[2],
                                                'Avg Decisions': avg_decisions,
                                                'Avg Solve Time': avg_solve_time,
                                                'OPTIMAL Count': count_optimal,
                                                'UNKNOWN Count': count_unknown},
                                               ignore_index=True)

            # If the file is a directory, recursively process it
            elif os.path.isdir(file_path):
                results_df = results_df.append(process_directory(file_path), ignore_index=True)

        return results_df


    # Provide the path to the mother directory
    mother_directory = 'results\j60-greedy'

    # Process the mother directory and get the results
    results = process_directory(mother_directory)

    # Display the results as a table
    print(results)
