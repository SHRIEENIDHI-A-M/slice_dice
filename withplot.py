import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load sample dataset (replace with your own)
# df = sns.load_dataset("tips") 
df = pd.read_csv("C:/Users/shrieenidhi.am/Downloads/current_purchase.csv")

st.title("Dynamic Data Explorer with Multiple Plots")

if st.checkbox("Show Raw Data"):
    st.dataframe(df)

with st.expander("🔎 Dataset Overview"):
    st.write("**Shape of dataset:**", df.shape)
    st.write("**Column names and types:**")
    st.dataframe(df.dtypes.astype(str))

    st.write("**Missing values:**")
    st.dataframe(df.isnull().sum())

    st.write("**Unique values per column:**")
    unique_vals = pd.DataFrame({col: [df[col].nunique()] for col in df.columns}).T
    unique_vals.columns = ['Unique Count']
    st.dataframe(unique_vals)

st.text("statistical information of the dataset")

with st.expander("Summary Statistics"):
    # st.dataframe(df.info())
    st.dataframe(df.describe(include='all'))

# Select plot type
plot_type = st.selectbox("Choose Plot Type", [
    "Scatter Plot",
    "Box Plot",
    "Histogram",
    "Bar Chart",
    "Line Plot"
])

# Select primary column(s)
x_col = st.selectbox("Select X-axis", df.columns)
y_col = st.selectbox("Select Y-axis (if applicable)", ['None'] + list(df.columns))
group_col = st.selectbox("Group by (optional)", ['None'] + list(df.columns))

# Set up plot
fig, ax = plt.subplots(figsize=(10, 6))

try:
    # Scatter Plot
    if plot_type == "Scatter Plot":
        if y_col != 'None':
            sns.scatterplot(data=df, x=x_col, y=y_col, hue=group_col if group_col != 'None' else None, ax=ax)

    # Box Plot
    elif plot_type == "Box Plot":
        if y_col != 'None':
            sns.boxplot(data=df, x=x_col, y=y_col, hue=group_col if group_col != 'None' else None, ax=ax)

    # Histogram
    elif plot_type == "Histogram":
        sns.histplot(data=df, x=x_col, hue=group_col if group_col != 'None' else None, kde=True, ax=ax)

    # Bar Chart (use count)
    elif plot_type == "Bar Chart":
        if group_col != 'None':
            count_df = df.groupby([x_col, group_col]).size().reset_index(name='count')
            sns.barplot(data=count_df, x=x_col, y='count', hue=group_col, ax=ax)
        else:
            count_df = df[x_col].value_counts().reset_index()
            count_df.columns = [x_col, 'count']
            sns.barplot(data=count_df, x=x_col, y='count', ax=ax)

    # Line Plot
    elif plot_type == "Line Plot":
        if y_col != 'None':
            sns.lineplot(data=df, x=x_col, y=y_col, hue=group_col if group_col != 'None' else None, ax=ax)

    st.pyplot(fig)

except Exception as e:
    st.error(f"Error generating plot: {e}")
