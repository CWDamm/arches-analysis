import AnalysisDashboard from '@/analysis/AnalysisDashboard.vue';
import createVueApplication from 'arches/arches/app/media/js/utils/create-vue-application';

console.log("Mounting...");

createVueApplication(AnalysisDashboard).then(vueApp => {
    vueApp.mount('#analysis-container');
});