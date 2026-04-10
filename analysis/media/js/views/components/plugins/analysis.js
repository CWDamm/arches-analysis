import ko from 'knockout';
import createVueApplication from 'arches/arches/app/media/js/utils/create-vue-application';
import AnalysisTemplate from 'templates/views/components/plugins/analysis.htm';
import AnalysisDashboard from '@/analysis/AnalysisDashboard.vue';

export default ko.components.register('analysis', {
    viewModel: function() {

        console.log("View Model");

        createVueApplication(AnalysisDashboard).then(vueApp => {
            vueApp.mount('#analysis-container');
        });
    },
    template: AnalysisTemplate
});