import sqlparse
from pyvis.network import Network

def parse_sql_query(query):
    # Format the SQL query for better readability
    formatted_query = sqlparse.format(query, reindent=True, keyword_case='upper')
    parsed = sqlparse.parse(formatted_query)[0]

    tables = []
    columns = []
    joins = []

    # Extract tokens from the SQL query
    for token in parsed.tokens:
        if token.ttype is None:
            if token.get_real_name():  # Columns
                columns.append(token.get_real_name())
            if token.get_parent_name():  # Tables
                tables.append(token.get_parent_name())
        elif token.value.upper() == "JOIN":
            joins.append(token)

    return {"tables": set(tables), "columns": set(columns), "joins": joins}


def create_graph(query_components):
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Add tables as nodes
    for table in query_components['tables']:
        net.add_node(table, label=table, color="blue")

    # Add columns as nodes
    for column in query_components['columns']:
        net.add_node(column, label=column, color="green")

    # Add relationships (joins)
    for table in query_components['tables']:
        for column in query_components['columns']:
            net.add_edge(table, column, color="white")

    return net


# Example SQL query
sql_query = """
SELECT studentname, teacher_salary 
FROM Student_info 
LEFT JOIN teachers_info 
ON Student_info.dept = teachers_info.department
"""

# Parse the query and create a graph
query_components = parse_sql_query(sql_query)
graph = create_graph(query_components)

# Save and display the graph
graph.show("sql_query_graph.html")
