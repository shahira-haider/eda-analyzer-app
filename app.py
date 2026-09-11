import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EDA Analyzer",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ===== BUTTON ===== */

    .stButton > button {
        background-color: #D6E6F7;
        color: #0A2540;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #DDE6ED;
        color: #1E3A8A;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"


# Check whether data has been uploaded
is_data_active = st.session_state.df is not None


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    "<h2 style='margin-bottom:-10px;'>📊 EDA ANALYZER</h2>",
    unsafe_allow_html=True
)
st.sidebar.info(
    "**Welcome!**\n\n"
    "Analyze your data. Discover meaningful insights."
)

st.sidebar.write("")


# ------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------

if st.sidebar.button(
    "📊 Dashboard",
    use_container_width=True,
    type="primary"
    if st.session_state.active_page == "Dashboard"
    else "secondary"
):
    st.session_state.active_page = "Dashboard"


# ------------------------------------------------------------
# DATA
# ------------------------------------------------------------

st.sidebar.markdown("**📂 DATA**")

if st.sidebar.button(
    "Preview",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Preview"
    else "secondary"
):
    st.session_state.active_page = "Preview"


if st.sidebar.button(
    "Overview",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Overview"
    else "secondary"
):
    st.session_state.active_page = "Overview"


if st.sidebar.button(
    "Complete Summary",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Summary"
    else "secondary"
):
    st.session_state.active_page = "Summary"


# ------------------------------------------------------------
# ANALYSIS
# ------------------------------------------------------------

st.sidebar.markdown("**📈 ANALYSIS**")

if st.sidebar.button(
    "Statistics",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Statistics"
    else "secondary"
):
    st.session_state.active_page = "Statistics"


if st.sidebar.button(
    "Correlation",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Correlation"
    else "secondary"
):
    st.session_state.active_page = "Correlation"


if st.sidebar.button(
    "Distribution",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Distribution"
    else "secondary"
):
    st.session_state.active_page = "Distribution"


if st.sidebar.button(
    "Outliers",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Outliers"
    else "secondary"
):
    st.session_state.active_page = "Outliers"


# ------------------------------------------------------------
# VISUALIZATION
# ------------------------------------------------------------

st.sidebar.markdown("**📊 VISUALIZATION**")

if st.sidebar.button(
    "Create Graph",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Create Graph"
    else "secondary"
):
    st.session_state.active_page = "Create Graph"


# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if st.session_state.active_page == "Dashboard":

    # --------------------------------------------------------
    # NO DATA
    # --------------------------------------------------------

    if not is_data_active:

        st.markdown(
            "<h1 style='text-align: center;'>📊 Dashboard</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align: center; color: gray;'>"
            "Get a quick overview of your dataset with key metrics, statistics, and insights."
            "</p>",
            unsafe_allow_html=True
        )

        st.write("")

        with st.container(border=True):

            uploaded_file = st.file_uploader(
                "Drag and drop your dataset file to unlock overview analytics",
                type=["csv", "xlsx", "xls"]
            )

            if uploaded_file is not None:

                try:

                    file_extension = (
                        uploaded_file.name
                        .split(".")[-1]
                        .lower()
                    )

                    if file_extension == "csv":

                        data = pd.read_csv(uploaded_file)

                    elif file_extension in ["xlsx", "xls"]:

                        data = pd.read_excel(uploaded_file)

                    else:

                        st.error("Unsupported File Format.")
                        st.stop()


                    # Convert boolean columns to string
                    bool_cols = data.select_dtypes(
                        include=["bool"]
                    ).columns

                    data[bool_cols] = data[bool_cols].astype("str")


                    # Save dataset
                    st.session_state.df = data
                    st.session_state.file_name = uploaded_file.name

                    st.success("✅ File uploaded successfully!")

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Could not read the CSV / Excel file. "
                        "Please check the file format."
                    )

                    st.exception(e)


    # --------------------------------------------------------
    # DATA LOADED
    # --------------------------------------------------------

    else:

        data = st.session_state.df

        st.markdown(
            "<h1 style='text-align: center;'>📊 Dashboard</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align: center; color: gray;'>"
            "Get a quick overview of your dataset and its key information."
            "</p>",
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            f"<p style='text-align: center; font-weight: bold;'>"
            f"Dataset: 📄 {st.session_state.file_name}"
            f"</p>",
            unsafe_allow_html=True
        )

        st.write("")


        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)

        with col_m1:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "🗂️ Rows"
                    "</p>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"## **{data.shape[0]:,}**"
                )


        with col_m2:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "📋 Columns"
                    "</p>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"## **{data.shape[1]}**"
                )


        with col_m3:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "❗ Missing"
                    "</p>",
                    unsafe_allow_html=True
                )

                total_missing = data.isna().sum().sum()

                st.markdown(
                    f"## **{total_missing:,}**"
                )


        with col_m4:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "🗄️ Duplicates"
                    "</p>",
                    unsafe_allow_html=True
                )

                total_dups = data.duplicated().sum()

                st.markdown(
                    f"## **{total_dups:,}**"
                )


        st.divider()


        # ----------------------------------------------------
        # DATASET OVERVIEW
        # ----------------------------------------------------

        st.markdown(
                    '<h3 style="text-align: center; margin-top: 20px; margin-bottom: 25px;">'
                    'Dataset Overview'
                    '</h3>',
                    unsafe_allow_html=True
                    )

        # Calculate Values
        num_cols_count = len (data.select_dtypes(include=[np.number]).columns)
        cat_cols_count = len(data.select_dtypes(include=["object","category"]).columns)

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                "<p style='text-align: center; color: gray;'>"
                "Numerical Columns"
                "</p>",
                unsafe_allow_html=True
                )

            st.markdown(
                f"<h2 style='text-align: center;'>{num_cols_count}</h2>",
                unsafe_allow_html=True
                )
            

        with col_right:
            st.markdown(
                "<p style='text-align: center; color: gray;'>"
                "Categorical Columns"
                "</p>",
                unsafe_allow_html=True
                )

            st.markdown(
                f"<h2 style='text-align: center;'>{cat_cols_count}</h2>",
                unsafe_allow_html=True
                )

        st.divider()


        # ----------------------------------------------------
        # DATASET INSIGHTS
        # ----------------------------------------------------   

        st.markdown(
            '<h3 style="text-align: center; margin-top: 20px; margin-bottom: 25px;">'
            'Dataset Insights'
            '</h3>',
            unsafe_allow_html=True
            )

        # Total number of cells 
        total_values = data.shape[0] * data.shape[1]

        # Total missing values
        total_missing = data.isna().sum().sum()

        # Missing value rate
        missing_rate = (
            (total_missing / total_values) * 100
            if total_values > 0
            else 0
            )

        # Memory usage
        memory_usage = data.memory_usage(deep=True).sum() / 1024

        # Mising values for each column 
        missing_by_column = data.isna().sum()

        # Most missing values
        missing_counts = data.isnull().sum()

        if missing_counts.max() == 0:
            most_missing = "None"
            most_missing_count = 0
        else:
            most_missing = missing_counts.idxmax()
            most_missing_count = missing_counts.max()

        # ----------------------------------------------------
        # INSIGHT METRICS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            with st.container(border=True):
                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "📊 Total Values"
                    "</p>",
                    unsafe_allow_html=True
                    )
                
                st.markdown(f"## **{total_values:,}**")

        with col2:
            with st.container(border=True):
                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "⚠️ Missing Rate"
                    "</p>",
                    unsafe_allow_html=True
                    )
       
                st.markdown(f"## **{missing_rate:.1f}%**")
            

        with col3:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "💾 Memory Usage"
                    "</p>",
                    unsafe_allow_html=True
                    )

                st.markdown(f"## **{memory_usage:.1f} KB**")

        with col4:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "❗ Most Missing"
                    "</p>",
                    unsafe_allow_html=True
                    )

                if most_missing == "None":
                    st.markdown("## **None**")

                else:
                    st.markdown(f"## **{most_missing}**")

        st.divider()


        # ----------------------------------------------------
        # RESET DATASET
        # ----------------------------------------------------      

        st.write("")      

        if st.button(
            "🔄 Reset / Upload Different Dataset",
            type="secondary",
            use_container_width=True
        ):

            st.session_state.df = None
            st.session_state.file_name = ""
            st.session_state.active_page = "Dashboard"

            st.rerun()


# ============================================================
# PAGE 2 — PREVIEW
# ============================================================

elif st.session_state.active_page == "Preview":

    data = st.session_state.df

    rows_to_show = min(20, len(data))

    st.markdown(
       "<h1 style='text-align: center;'>🗃️ Dataset Preview</h1>",
        unsafe_allow_html=True)

    st.markdown(
       "<p style='text-align: center; color: gray;'>"
        "Take a quick look at your dataset and explore its contents."
        "</p>",
        unsafe_allow_html=True)

    st.write("")


    st.caption(
        f"Showing first {rows_to_show} of {len(data):,} rows"
    )

    st.dataframe(
        data.head(rows_to_show),
        use_container_width=True
    )

    st.write(
        f"**Shape:** {data.shape[0]:,} rows × "
        f"{data.shape[1]:,} columns"
    )


# ============================================================
# PAGE 3 — OVERVIEW
# ============================================================

elif st.session_state.active_page == "Overview":

    data = st.session_state.df

    st.markdown(
        "<h1 style='text-align: center;'>🔎 Dataset Overview</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "View your dataset structure, including column names, "
        "data types, and non-null values."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("### 📋 Column Information")
    st.caption("Review each column's data type and the number of non-null values.")

    dtypes_df = pd.DataFrame({
        "Column Name": data.columns,
        "Data Type": [str(t) for t in data.dtypes],
        "Non-Null Count": data.notna().sum().values
    })

    st.dataframe(
        dtypes_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 4 — COMPLETE SUMMARY
# ============================================================

elif st.session_state.active_page == "Summary":

    data = st.session_state.df

    st.markdown(
        "<h1 style='text-align: center;'>📝 Complete Summary</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "View detailed information about your dataset, including "
        "its structure, data types, and memory usage."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("### 📊 Dataset Information")
    st.caption("A complete summary of your dataset.")

    buffer = io.StringIO()

    data.info(buf=buffer)

    information = buffer.getvalue()

    st.code(information)


# ============================================================
# PAGE 5 — STATISTICS
# ============================================================


elif st.session_state.active_page == "Statistics":

    data = st.session_state.df

    st.markdown(
        "<h1 style='text-align: center;'>📈 Statistical Analysis</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Analyze numerical and non-numerical features with "
        "statistical summaries and unique value counts."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")
    #st.divider()

    # --------------------------------------------------------
    # NUMERICAL
    # --------------------------------------------------------

    st.subheader("🔢 Statistical Summary")
    st.caption("Get a statistical overview of your numerical features.")

    numeric_data = data.select_dtypes(
        include="number"
    )

    if not numeric_data.empty:

        st.dataframe(
            numeric_data.describe(),
            use_container_width=True
        )

    else:

        st.info(
            "No numerical features found in this dataset."
        )

    st.divider()


    # --------------------------------------------------------
    # NON-NUMERICAL
    # --------------------------------------------------------

    st.subheader("🔤 Statistical Summary For Non-Numerical Features")
    st.caption("Explore key statistics for your categorical and text-based features")

    non_numerical = data.select_dtypes(
        include=["bool", "object", "category"]
    )

    if not non_numerical.empty:

        st.dataframe(
            non_numerical.describe(),
            use_container_width=True
        )

    else:

        st.info(
            "No non-numerical features found."
        )

    st.divider()


    # --------------------------------------------------------
    # UNIQUE VALUES
    # --------------------------------------------------------

    st.subheader("📌 Unique Values")
    st.caption("View the number of unique values in each feature.")

    unique_values = data.nunique()

    unique_df = unique_values.reset_index()

    unique_df.columns = [
        "Columns",
        "Unique Values"
    ]

    st.dataframe(
        unique_df,
        use_container_width=True,
        hide_index=True
    )



# ============================================================
# PAGE 6 — CORRELATION
# ============================================================

elif st.session_state.active_page == "Correlation":

    data = st.session_state.df

    st.markdown(
        "<h1 style='text-align: center;'>🔗 Correlation Matrix</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "View the correlation between numerical features in your dataset."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")
    #st.divider()

    numeric_data = data.select_dtypes(
        include="number"
    )

    if len(numeric_data.columns) > 1:

        correlation = numeric_data.corr()

        

        st.subheader("Correlation Table")

        st.dataframe(
            correlation,
            use_container_width=True
        )


        if st.button(
            "📈 Generate Correlation Heatmap"
        ):

            fig, ax = plt.subplots(
                figsize=(10, 8)
            )

            heatmap = ax.imshow(
                correlation,
                cmap="coolwarm",
                vmin=-1,
                vmax=1
            )

            plt.colorbar(heatmap)


            ax.set_xticks(
                range(len(correlation.columns))
            )

            ax.set_yticks(
                range(len(correlation.columns))
            )

            ax.set_xticklabels(
                correlation.columns,
                rotation=45,
                ha="right"
            )

            ax.set_yticklabels(
                correlation.columns
            )


            for i in range(
                len(correlation.columns)
            ):

                for j in range(
                    len(correlation.columns)
                ):

                    ax.text(
                        j,
                        i,
                        f"{correlation.iloc[i, j]:.2f}",
                        ha="center",
                        va="center",
                        color="black"
                    )


            ax.set_title(
                "Correlation Heatmap"
            )

            plt.tight_layout()

            st.pyplot(fig)

    else:

        st.info(
            "Correlation matrix requires at least "
            "two numerical columns."
        )


# ============================================================
# PAGE 7 — DISTRIBUTION
# ============================================================

elif st.session_state.active_page == "Distribution":

    data = st.session_state.df

    st.markdown(
        "<h1 style='text-align: center;'>📉 Data Distribution</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Explore the distribution and patterns of numerical features "
        "in your dataset."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    numeric_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()

    if len(numeric_columns) == 0:

        st.warning(
            "No numerical columns found."
        )

    else:

        selected_column = st.selectbox(
            "Select Numerical Column",
            numeric_columns
        )

        st.write("")

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.hist(
            data[selected_column].dropna(),
            bins=20
        )

        ax.set_xlabel(
            selected_column
        )

        ax.set_ylabel(
            "Frequency"
        )

        ax.set_title(
            f"Distribution of {selected_column}"
        )

        st.pyplot(fig)


# ============================================================
# PAGE 8 — OUTLIERS
# ============================================================

elif st.session_state.active_page == "Outliers":

    data = st.session_state.df

    st.markdown(
        "<h1 style='text-align: center;'>📈 Outlier Analysis</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Identify unusual values and potential outliers "
        "in your numerical features."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("🔎 Outlier Detection")

    numeric_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()

    if len(numeric_columns) == 0:

        st.warning(
            "No numerical columns found for outlier analysis."
        )

    else:

        selected_column = st.selectbox(
            "Select Numerical Column",
            numeric_columns
        )

        st.write("")

        # --------------------------------------------------------
        # OUTLIER CALCULATION
        # --------------------------------------------------------

        values = data[selected_column].dropna()

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = values[
            (values < lower_bound) |
            (values > upper_bound)
        ]

        outlier_count = len(outliers)

        outlier_percentage = (
            outlier_count / len(values) * 100
            if len(values) > 0
            else 0
        )

        # --------------------------------------------------------
        # IQR INFORMATION
        # --------------------------------------------------------

        st.write("")
        st.write("**📊 IQR Information**")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Q1",
                f"{q1:,.2f}"
            )

        with col2:
            st.metric(
                "Q3",
                f"{q3:,.2f}"
            )

        with col3:
            st.metric(
                "IQR",
                f"{iqr:,.2f}"
            )

        with col4:
            st.metric(
                "Outliers",
                f"{outlier_count:,}"
            )

        st.write("")

        # --------------------------------------------------------
        # BOUNDS
        # --------------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"**Lower Bound:** {lower_bound:,.2f}"
            )

        with col2:
            st.info(
                f"**Upper Bound:** {upper_bound:,.2f}"
            )

        st.write("")

        st.caption(
            f"Outlier Percentage: {outlier_percentage:.2f}%"
        )

        st.divider()
        #st.write("")

        # --------------------------------------------------------
        # OUTLIER VALUES
        # --------------------------------------------------------

        #st.write(f"Outliers Found: **{len(outliers)}**")
        st.subheader("**📌 Outlier Values**")

        if outlier_count == 0:

            st.success(
                "✅ No outliers detected in this column."
            )

        else:

            #st.caption(f"Outliers detected using the IQR method.")
            st.caption(
                f"{outlier_count:,} outlier(s) detected "
                f"using the IQR method.")

            outlier_df = pd.DataFrame({
                selected_column: outliers
            })

            st.dataframe(
                outlier_df,
                use_container_width=True
            )

            #st.divider()
            #st.write("")

        # --------------------------------------------------------
        # BOXPLOT
        # --------------------------------------------------------

        st.divider()
        #st.write("")

        st.subheader("📦 Outlier Visualization")
        st.caption("Use the boxplot to identify the spread and potential outliers.")

        fig, ax = plt.subplots(figsize=(10,5))

        sns.boxplot(
            y=data[selected_column],
            ax=ax
        )

        ax.set_title(f"Boxplot of {selected_column}")

        ax.set_ylabel(selected_column)

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# PAGE 9 — CREATE GRAPH
# ============================================================

elif st.session_state.active_page == "Create Graph":

    data = st.session_state.df

    st.markdown(
        "<h1 style='text-align: center;'>📊 Data Visualization</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Explore your dataset through interactive charts and visual representations."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    numeric_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = data.select_dtypes(
        include=["object", "bool", "category"]
    ).columns.tolist()


    graph = st.selectbox(
        "Select A Graph",
        [
            "📈 Line Graph",
            "🔵 Scatter Plot",
            "📊 Bar Graph",
            "🥧 Pie Chart",
            "📋 Count Plot"
        ]
    )


    # ========================================================
    # LINE GRAPH
    # ========================================================

    if graph == "📈 Line Graph":

        if len(numeric_columns) < 2:

            st.warning(
                "Line Graph requires at least "
                "two numerical columns."
            )

        else:

            x_axis = st.selectbox(
                "Select X-axis",
                numeric_columns,
                key="line_x"
            )

            remaining_columns = [
                col
                for col in numeric_columns
                if col != x_axis
            ]

            y_axis = st.selectbox(
                "Select Y-axis",
                remaining_columns,
                key="line_y"
            )

            fig, ax = plt.subplots()

            ax.plot(
                data[x_axis],
                data[y_axis]
            )

            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)

            ax.set_title(
                f"{x_axis} vs {y_axis}"
            )

            st.pyplot(fig)


    # ========================================================
    # SCATTER PLOT
    # ========================================================

    elif graph == "🔵 Scatter Plot":

        if len(numeric_columns) < 2:

            st.warning(
                "Scatter Plot requires at least "
                "two numerical columns."
            )

        else:

            x_axis = st.selectbox(
                "Select X-axis",
                numeric_columns,
                key="scatter_x"
            )

            remaining_columns = [
                col
                for col in numeric_columns
                if col != x_axis
            ]

            y_axis = st.selectbox(
                "Select Y-axis",
                remaining_columns,
                key="scatter_y"
            )

            fig, ax = plt.subplots()

            ax.scatter(
                data[x_axis],
                data[y_axis],
                s=25
            )

            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)

            ax.set_title(
                f"{x_axis} vs {y_axis}"
            )

            st.pyplot(fig)


    # ========================================================
    # BAR GRAPH
    # ========================================================

    elif graph == "📊 Bar Graph":

        if len(categorical_columns) == 0:

            st.warning(
                "No categorical columns found "
                "for the X-axis."
            )

        elif len(numeric_columns) == 0:

            st.warning(
                "No numerical columns found "
                "for the Y-axis."
            )

        else:

            x_axis = st.selectbox(
                "Select X-axis",
                categorical_columns,
                key="bar_x"
            )

            y_axis = st.selectbox(
                "Select Y-axis",
                numeric_columns,
                key="bar_y"
            )

            grouped = (
                data.groupby(x_axis)[y_axis]
                .mean()
            )

            fig, ax = plt.subplots()

            ax.bar(
                grouped.index.astype(str),
                grouped.values
            )

            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)

            ax.set_title(
                f"Average {y_axis} by {x_axis}"
            )

            ax.tick_params(
                axis="x",
                labelrotation=45
            )

            plt.tight_layout()

            st.pyplot(fig)


    # ========================================================
    # PIE CHART
    # ========================================================

    elif graph == "🥧 Pie Chart":

        if len(categorical_columns) == 0:

            st.warning(
                "No categorical columns found "
                "for Pie Chart."
            )

        else:

            selected_column = st.selectbox(
                "Select Categorical Column",
                categorical_columns,
                key="pie_column"
            )

            value_counts = (
                data[selected_column]
                .value_counts()
            )

            fig, ax = plt.subplots(
                figsize=(8, 8)
            )

            ax.pie(
                value_counts.values,
                labels=value_counts.index,
                autopct="%1.1f%%"
            )

            ax.set_title(
                f"Distribution of {selected_column}"
            )

            st.pyplot(fig)


    # ========================================================
    # COUNT PLOT
    # ========================================================

    elif graph == "📋 Count Plot":

        if len(categorical_columns) == 0:

            st.warning(
                "No categorical columns found "
                "for Count Plot."
            )

        else:

            selected_column = st.selectbox(
                "Select Categorical Column",
                categorical_columns,
                key="count_column"
            )

            fig, ax = plt.subplots(
                figsize=(10, 5)
            )

            sns.countplot(
                data=data,
                x=selected_column,
                ax=ax
            )

            ax.set_title(
                f"Count Plot of {selected_column}"
            )

            ax.tick_params(
                axis="x",
                labelrotation=45
            )

            plt.tight_layout()

            st.pyplot(fig)