<script setup>
import { ref, watch } from "vue";

const graph_objects = ref([]);
const concept_nodes = ref([]);
const selectedGraphId = ref("");
const selectedNode = ref("");


fetch("/graphs")
    .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch graphs");
        return response.json();
    })
    .then((data) => {
        graph_objects.value = data.filter(
            (graph) => graph.graphid != "ff623370-fa12-11e6-b98b-6c4008b05c4c",
        );
    })
    .catch((err) => console.error(err));

watch(selectedGraphId, (newGraphId) => {
    if (!newGraphId) return;

    fetch(`/graph/${newGraphId}/nodes`)
        .then((response) => {
            if (!response.ok) throw new Error("Failed to fetch nodes");
            return response.json();
        })
        .then((data) => {
            concept_nodes.value = Object.values(data).filter(
                (node) => node["datatype"] === "concept",
            );
        })
        .catch((err) => console.error("Error fetching nodes:", err));
});

function handleClick() {
  console.log("Button was clicked!");
}
</script>

<template>
    <div class="analysis-dashboard">
        <div class="control-panel">
            <select v-model="selectedGraphId" class="drop-down">
                <option value="" disabled>Select a resource model...</option>
                <option 
                    v-for="graph in graph_objects" 
                    :key="graph.graphid" 
                    :value="graph.graphid"
                >
                    {{ graph.name }}
                </option>
            </select>

            <select v-model="selectedNode" :disabled="!selectedGraphId" class="drop-down">
                <option value="">Select a concept node...</option>
                <option 
                    v-for="node in concept_nodes" 
                    :key="node.name" 
                    :value="node.name"
                >
                    {{ node.name }}
                </option>
            </select>
            <button @click="handleClick">
                Fetch results
            </button>
        </div>
    </div>
</template>

<style>
    .analysis-dashboard{
        height: 100%;
        border: 1px solid red; 
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .control-panel{
        border: 1px solid green;
        padding: 20px;
        display: flex;
        flex-direction: column;
    }

    .drop-down{
        border: 1px blue;
        margin-bottom: 10px;
        width: 200px;
        background-color: white;
    }
</style>    
