<script setup>
import { ref, watch, computed, onMounted } from "vue";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { Bar } from 'vue-chartjs';

const graph_objects = ref([]);
const concept_nodes = ref([]);
const selectedGraphId = ref("");
const selectedNode = ref("");
const countsData = ref({});
const isLoadingGraphs = ref(false);

ChartJS.register(Title, Tooltip, BarElement, CategoryScale, LinearScale);

const chartData = computed(() => {
    return{
        labels: Object.keys(countsData.value),
        datasets: [
            {
            label: 'Count',
            backgroundColor: '#42b883',
            data: Object.values(countsData.value)
            },
        ]
    }
});

const chartOptions = ref({
    responsive: true,
    scales: {
        y: { beginAtZero: true }
    },
    indexAxis: 'y',
});

const totalCount = computed(() => {
  return Object.values(countsData.value).reduce((sum, count) => sum + count, 0);
});

const tableRows = computed(() => {
  if (totalCount.value === 0) return [];
  
  return Object.entries(countsData.value).map(([category, count]) => {
    const pct = (count / totalCount.value) * 100;
    return {
      category,
      count,
      percentage: pct.toFixed(1) 
    };
  });
});

async function fetchGraphs() {
    isLoadingGraphs.value = true;
    try {
        const response = await fetch("/graphs");
        if (!response.ok) throw new Error("Failed to fetch graphs");
        
        const data = await response.json();
        graph_objects.value = data.filter(
            (graph) => graph.graphid !== "ff623370-fa12-11e6-b98b-6c4008b05c4c"
        );
    } catch (err) {
        console.error("Error fetching graphs:", err);
    } finally {
        isLoadingGraphs.value = false;
    }
}

onMounted(() => {
    fetchGraphs();
});

watch(selectedGraphId, (newGraphId) => {

    selectedNode.value = "";
    concept_nodes.value = [];
    countsData.value = {}

    if (!newGraphId) return;

    fetch(`/graph/${newGraphId}/nodes`)
        .then((response) => {
            if (!response.ok) throw new Error("Failed to fetch nodes");
            return response.json();
        })
        .then((data) => {
            selectedNode.value = "";
            concept_nodes.value = Object.values(data).filter(
                (node) => node["datatype"] === "concept",
            );
        })
        .catch((err) => console.error("Error fetching nodes:", err));
});

function handleClick() {
    if (!selectedNode.value) {
        console.warn("Please select a concept node before fetching.");
        return;
    }

    fetch(`/analysis/${selectedNode.value}`)
        .then((response) => {
            if (!response.ok) throw new Error("Failed to fetch value count");
            return response.json();
        })
        .then((data) => {
            countsData.value = data;
        })
        .catch((err) => console.error("Error fetching value count:", err));
}
</script>

<template>

    <div class="analysis-dashboard">

        <div class="count-control-panel">
            <select v-model="selectedGraphId" :disabled="isLoadingGraphs" class="table-select">
                <option value="" disabled>Select a resource model...</option>
                <option 
                    v-for="graph in graph_objects" 
                    :key="graph.graphid" 
                    :value="graph.graphid"
                >
                    {{ graph.name }}
                </option>
            </select>

            <select v-model="selectedNode" :disabled="!selectedGraphId" class="table-select">
                <option value="">Select a concept node...</option>
                <option 
                    v-for="node in concept_nodes" 
                    :key="node.nodeid" 
                    :value="node.nodeid"
                >
                    {{ node.name }}
                </option>
            </select>

            <button @click="handleClick">
                Fetch results
            </button>

        </div>

            <div class="results-container" v-if="Object.keys(countsData).length > 0" >
            
                <div class="table-panel">
                    <table>
                        <thead>
                            <tr>
                                <th>Category</th>
                                <th>Count</th>
                                <th>Percent</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="row in tableRows" :key="row.category">
                                <td>{{ row.category }}</td>
                                <td>{{ row.count }}</td>
                                <td>{{ row.percentage }}%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div style="max-width: 600px;" class="chart-panel">
                    <Bar :data="chartData" :options="chartOptions" />
                </div>

            </div>

    </div>

</template>

<style scoped>
    .analysis-dashboard{
        height: 100%;
        display: flex;
        justify-content: start;
        align-items: center;
        flex-direction: column;
    }

    .count-control-panel{
        border: 1px solid grey;
        padding: 20px;
        display: flex;
        flex-direction: row;
        width: 100%;
        justify-content: start;
        background-color: #fafaf9;
    }

    .count-control-panel select{
        border: 1px solid grey;
        width: 250px;
        height: 30px;
        background-color: white;
        margin-right: 25px;
    }

    .count-control-panel select:focus-visible {
        outline: none !important;
        border-color: grey;
    }

    .count-control-panel select:focus {
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
    }

    .results-container{
        border: 1px solid lightgrey;
        display: flex;
        flex-direction: row;
        padding: 30px;
    }

    .chart-panel{
        border: 1px solid lightgrey;
        padding: 15px;
        background-color: #fafaf9;
    }

    .table-panel{
        border: 1px solid lightgrey;
        padding: 20px;
        margin-right: 40px;
        background-color: #fafaf9;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 8px 12px;
        text-align: left;
    }

    th {
        background-color: #f4f4f4;
    }

</style>    
