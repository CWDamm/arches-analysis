<script setup>
import { ref, watch } from "vue";

const graph_objects = ref([]);
const concept_nodes = ref([]);
const selectedGraphId = ref("");

fetch("/graphs")
    .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch graphs");
        return response.json();
    })
    .then((data) => {
        console.log(data);
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
    <div>
        <select
            id="graph-select"
            v-model="selectedGraphId"
        >
            <option
                disabled
                value=""
            >
                Choose a graph...
            </option>
            <option
                v-for="graph in graph_objects"
                :key="graph.graphid"
                :value="graph.graphid"
            >
                {{ graph.name }}
            </option>
        </select>
    </div>

    <div v-if="selectedGraphId">
        <select id="node-select">
            <option
                v-for="node in concept_nodes"
                :key="node.nodegroup_id"
                :value="node.nodegroup_id"
            >
                {{ node.name }}
            </option>
        </select>
    </div>
</template>

<style scoped>
button {
    font-weight: bold;
}
</style>
