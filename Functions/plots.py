import plotly.graph_objects as go

#---- Plot the return of the project with the visualisation of the return and the pourcentage compared to the investment

def differents_returns(json_file,investisment):
    returns = []
    ways = []
    labels, labels2= [],[]
    investisment_pourcentage=[]
    for i in range(len(json_file["ways"])):
        returns.append(json_file["ways"][i]["return"])
        ways.append(str(i+1))
        labels.append(f"Best way n°{i+1}")
        investisment_pourcentage.append(json_file["ways"][i]["return"]/investisment)
        labels2.append(f'Best way n°{i+1} : {round(json_file["ways"][i]["return"]/investisment,4)}%')
    
    fig = go.Figure(
        data=go.Bar(
            x=ways,
            y=investisment_pourcentage,
            text='',#labels,
            name="Pourcentage of return",
            hovertemplate=labels2,
            marker=dict(color="rgb(105,105,105)", line=dict(color="rgb(0,0,0)", width=1)),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=ways,
            y=returns,
            yaxis="y2",
            mode='lines+markers', 
            text=labels,
            name="Evolution of the differents return",
            marker=dict(color="rgb(255,69,0)", line=dict(color="rgb(0,0,0)", width=1)),
        )
    )

    fig.update_layout(
       title='Evolution of Return', 
        xaxis_title='Way Index',
        legend=dict(x=0.42, y=0.98),
        showlegend=True,
        yaxis=dict(
            title=dict(text="Pourcentage of return"),
            side="right",
            range=[min(investisment_pourcentage)*0.9995, max(investisment_pourcentage)],
        ),
        yaxis2=dict(
            title=dict(text="Returns"),
            side="left",
            range=[round(min(returns))-1, round(max(returns))+1],
            overlaying="y",
            tickmode="sync",
        ),
    )
    return fig
