import boto3
import streamlit as streamlit

client = boto3.client('datapipeline', region_name='eu-west-1')  # Use your specific region


def list_pipelines(pipeline_id=None):
    response = client.list_pipelines()

    if not pipeline_id:
        pipelines = response.get('pipelineIdList', [])
        return pipelines
    else:
        pipelines_describe = client.describe_pipelines(pipelineIds=pipeline_id)
        return pipelines_describe


# Set a title for the application
streamlit.title("AWS Pipeline Viewer")

# Fetch and display the list of pipelines
pipelines = list_pipelines()

if pipelines:
    streamlit.subheader(f"Found {len(pipelines)} pipelines:")
    # Create a table view of pipeline names and IDs
    pipeline_names = [pipeline['name'] for pipeline in pipelines]
    pipeline_ids = [pipeline['id'] for pipeline in pipelines]

    pipeline_data = {
        "Pipeline Name": pipeline_names,
        "Pipeline ID": pipeline_ids
    }

    # Display pipelines as a dataframe in Streamlit
    streamlit.table(pipeline_data)

    # Let the user select a pipeline for more details
    selected_pipeline = streamlit.selectbox("Select a pipeline to view details", pipeline_names)

    # Find the selected pipeline ID
    selected_pipeline_id = [pipeline['id'] for pipeline in pipelines if pipeline['name'] == selected_pipeline][0]

    # Describe the selected pipeline and show details
    if selected_pipeline:
        streamlit.subheader(f"Details for {selected_pipeline}")
        pipeline_details = list_pipelines([selected_pipeline_id])

        # Now safely check if the expected data is there
        if 'pipelineDescriptionList' in pipeline_details and pipeline_details['pipelineDescriptionList']:
            for field in pipeline_details['pipelineDescriptionList'][0]['fields']:
                streamlit.write(f"{field['key']}: {field.get('stringValue', '')}")
        else:
            streamlit.write("No pipeline description found.")

else:
    streamlit.write("No pipelines found.")
