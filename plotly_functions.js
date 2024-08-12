// Sample Spotify song data with clustering labels
const songs = [
    {id: 1, popularity: 0.5, duration_ms: 60000*5, cluster: 0},
    {id: 2, popularity: 0.6, duration_ms: 60000*3.3, cluster: 0},
    {id: 3, popularity: 0.1, duration_ms: 60000*2.3, cluster: 1},
    {id: 4, popularity: 0.2, duration_ms: 60000*6, cluster: 1},
    {id: 5, popularity: 0.8, duration_ms: 60000*3.5, cluster: 2},
    {id: 6, popularity: 0.9, duration_ms: 60000*2, cluster: 2}
];

// Group data by cluster
const clusterData = {};
songs.forEach(song => {
    if (!clusterData[song.cluster]) {
        clusterData[song.cluster] = { x: [], y: [], text: [] };
    }
    clusterData[song.cluster].x.push(song.popularity);
    clusterData[song.cluster].y.push(song.duration_ms);
    clusterData[song.cluster].text.push(`Song ID: ${song.id}`);
});

// Prepare traces for each cluster
const traces = Object.keys(clusterData).map(cluster => {
    return {
        x: clusterData[cluster].x,
        y: clusterData[cluster].y,
        mode: 'markers',
        type: 'scatter',
        name: `Cluster ${cluster}`,
        text: clusterData[cluster].text,
        marker: { size: 12 }
    };
});

const layout = {
    title: 'Spotify Song Clusters',
    xaxis: { title: 'Popularity' },
    yaxis: { title: 'Duration_ms' },
    showlegend: true
};

// Plot the clusters
Plotly.newPlot('myPlot', traces, layout);