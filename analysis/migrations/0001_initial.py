from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    forward = """
        INSERT INTO plugins (
            pluginid, name, icon, component, componentname, config, slug, sortorder)
        VALUES (
            '6fde0fcd-0a78-4110-9428-b8181ad6bd1e',
            '{"en": "Analysis"}',
            'fa fa-chart-line', 
            'views/components/plugins/analysis',
            'analysis', 
            '{"show": true, "is_workflow": false, "description": ""}',
            'analysis',
            '1'
        );
        """
    
    reverse = """
        DELETE FROM plugins where pluginid = '6fde0fcd-0a78-4110-9428-b8181ad6bd1e';
        """
    
    operations = [
        migrations.RunSQL(forward, reverse),
    ]
