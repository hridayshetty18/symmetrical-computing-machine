import networkx as nx
import plotly.graph_objects as go

def plot_fraud_network(df, selected_hospital=None):
    """
    Creates a basic network graph showing links between Hospitals and Patients.
    If selected_hospital is provided, it highlights its connections.
    """
    G = nx.Graph()
    
    # We will limit the graph to a subset for performance if df is large
    # Just take top 200 rows or filter by the selected hospital
    if selected_hospital:
        # Filter claims involving patients who visited this hospital
        patients = df[df['Hospital'] == selected_hospital]['Patient_ID'].unique()
        plot_df = df[df['Patient_ID'].isin(patients)]
    else:
        # Sample for overall view
        plot_df = df.head(150)
        
    for _, row in plot_df.iterrows():
        hosp = row['Hospital']
        pat = row['Patient_ID']
        status = row['Status']
        
        G.add_node(hosp, type='Hospital', color='blue', size=20)
        
        # Color patient red if any of their claims is fraud
        pat_color = 'red' if status == 'Suspected Fraud' else 'green'
        
        # If node exists, don't overwrite with green if it's already red
        if G.has_node(pat):
            if G.nodes[pat].get('color') == 'red':
                pat_color = 'red'
                
        G.add_node(pat, type='Patient', color=pat_color, size=10)
        G.add_edge(hosp, pat)
        
    # Generate layout
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_color = []
    node_size = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append(G.nodes[node]['color'])
        node_size.append(G.nodes[node]['size'])
        node_text.append(f"{G.nodes[node]['type']}: {node}")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=2))
            
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Hospital - Patient Network',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    return fig
