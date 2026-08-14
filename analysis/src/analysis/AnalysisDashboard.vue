<script setup>
import { ref, watch } from "vue";
import Select from 'primevue/select';

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
</script>

<template>
    <div class="analysis-dashboard">
        <div class="control-panel">
            <div>
                <Select 
                    id="graph-select"
                    class="drop-down"
                    v-model="selectedGraphId" 
                    :options="graph_objects" 
                    optionLabel="name" 
                    optionValue="graphid" 
                    placeholder="Choose a graph..." 
                />
            </div>

            <div v-if="selectedGraphId">
                <Select 
                    id="node-select"
                    class="drop-down"
                    v-model="selectedNode" 
                    :options="concept_nodes" 
                    optionLabel="name" 
                    optionValue="nodegroup_id" 
                    placeholder="Choose a node..." 
                />
            </div>
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
    }

    .drop-down{
        border: 1px blue;
        margin-bottom: 10px;
    }
</style>    
