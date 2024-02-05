# Required Libraries
import os
from lxml import etree
import pandas as pd
import streamlit as st

# Function to get a dictionary of XPaths and values from an XML file
def get_xpaths_and_values(xml_content):
    tree = etree.fromstring(xml_content)
    root = etree.ElementTree(tree) # Creating an ElementTree object
    xpaths_and_values = {root.getpath(e): e.text for e in tree.iter()} # Using the root object to call getpath
    return xpaths_and_values

# Function to compare two sets of XML files
def compare_xml_files(release_files, production_files):
    differences = []

    # Compare XML files in both sets
    for file_name, release_file_content in release_files.items():
        if file_name in production_files:
            production_file_content = production_files[file_name]
            release_xpaths_and_values = get_xpaths_and_values(release_file_content)
            production_xpaths_and_values = get_xpaths_and_values(production_file_content)
            for xpath in set(release_xpaths_and_values.keys()).union(production_xpaths_and_values.keys()):
                if release_xpaths_and_values.get(xpath) != production_xpaths_and_values.get(xpath):
                    differences.append([
                        'Differences', file_name, xpath,
                        production_xpaths_and_values.get(xpath), release_xpaths_and_values.get(xpath)
                    ])
        else:
            differences.append(['Missing in prod', file_name, None, None, None])

    # Check for files missing in release
    for file_name in production_files:
        if file_name not in release_files:
            differences.append(['Missing in release', file_name, None, None, None])

    return differences

# Streamlit app interface
def main():
    st.title("XML Reconciliation App 🧐")

    st.markdown("Upload XML files from **Release** and **Production** folders and compare the differences.")

    # Upload Release XML files
    release_files = st.file_uploader("Upload Release XML files:", type=["xml"], accept_multiple_files=True)
    release_files_dict = {file.name: file.read() for file in release_files}

    # Upload Production XML files
    production_files = st.file_uploader("Upload Production XML files:", type=["xml"], accept_multiple_files=True)
    production_files_dict = {file.name: file.read() for file in production_files}

    # Compare button
    if st.button("Compare"):
        if not release_files or not production_files:
            st.warning("Please upload XML files in both Release and Production sections!")
        else:
            differences = compare_xml_files(release_files_dict, production_files_dict)
            if differences:
                df = pd.DataFrame(differences, columns=['Status', 'File Name', 'xPath', 'Value in Production', 'Value Release'])
                st.dataframe(df)
                st.success("Comparison completed! 🎉")
            else:
                st.info("No differences found between the XML files. 🎉")

# Run the Streamlit app
if __name__ == "__main__":
    main()
