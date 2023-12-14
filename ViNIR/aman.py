import os
import pandas as pd
import matplotlib.pyplot as plt


def filter_csv_near_max_value(csv_file, target_column_index, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)  # Assuming there is no header in the CSV file

    # Find the index of the maximum value in the specified column
    max_value = df.iloc[:, target_column_index].max()

    # Normalize only the specified column by dividing by the maximum value
    df.iloc[:, target_column_index] = df.iloc[:, target_column_index] / max_value

    # Save the DataFrame to a new CSV file, keeping the 1st column unchanged
    df.to_csv(output_csv, index=False, header=False, mode='w', sep=',')



def process_files_in_folder(input_folder, output_folder, st_limit, end_limit):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Lists to store data for plotting
    all_data = []
    file_labels = []  # Store file names for labeling

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Check if the file is a CSV file
        if filename.endswith(".csv") and os.path.isfile(file_path):
            output_file_path = os.path.join(output_folder, f"filtered_{filename}")

            # Extract file name (excluding extension) for labeling
            file_label = os.path.splitext(filename)[0]
            file_labels.append(file_label)

            # Apply the filtering and normalization function to each CSV file
            filter_csv_near_max_value(file_path, 1, output_file_path)

            # Read the filtered CSV file for plotting
            filtered_data = pd.read_csv(output_file_path, header=None)

            # Append the data to the list for plotting
            all_data.append(filtered_data)

    # Plotting
    plt.figure(figsize=(10, 6))
    for i, data in enumerate(all_data):
        plt.plot(data.iloc[:, 0], data.iloc[:, 1], label=f'{file_labels[i]} nm')

    plt.xlim(st_limit, end_limit)
    plt.xlabel('Pixel Values')
    plt.ylabel('Normalized Intensity')
    plt.title('Curve Plot for vinir Data')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=6)
    plt.show()