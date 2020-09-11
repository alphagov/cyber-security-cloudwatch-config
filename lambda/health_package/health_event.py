""" Data model for health event data """
import json
import os


class HealthEvent:
    """ Create an event and handle convert to JSON nicely """

    def __init__(self):
        """ Create a default event """
        self.component_type = None
        self.source = "Unknown"
        self.environment = os.environ.get("DEF_ENVIRONMENT")
        self.notify_slack = True
        self.event_type = "Alarm/Metric"
        self.service = "Unknown"
        self.healthy = True
        self.resource = {}
        self.source_data = {}
        self.metric_data = None

    def populate(
        self,
        source=None,
        component_type=None,
        event_type=None,
        notify_slack=None,
        environment=None,
        service=None,
        healthy=None,
        resource_name=None,
        resource_id=None,
        source_data=None,
        metric_data=None,
    ):
        """" set all event properties as optional keywords"""
        args = locals()  # gets a dictionary of all local parameters
        set_resource = False
        for argument, val in args.items():
            if argument in ["resource_name", "resource_id"]:
                set_resource = set_resource or val is not None
            elif argument != "self" and val is not None:
                self.set_attribute(argument, val)

        if set_resource:
            self.set_resource(args["resource_name"], args["resource_id"])

    def set_attribute(self, attribute_name, value):
        """ Set an object attribute by name """
        setattr(self, attribute_name, value)

    def get_attribute(self, attribute_name):
        """ Get an object attribute by name """
        return getattr(self, attribute_name)

    def set_attributes(self, attributes):
        """ Set attributes from dictionary """
        for attr, val in attributes.items():
            # if hasattr(self, attr):
            if val is not None:
                self.set_attribute(attr, val)

    def set_source(self, source):
        """ Set the event source [ CloudWatch | Splunk | UptimeRobot | Concourse ] """
        if source is not None:
            self.source = source

    def set_component_type(self, component_type):
        """ Set the component type
            component_type = [ "AWS/SQS", "Concourse", "UptimeRobot"... ]
        """
        if component_type is not None:
            self.component_type = component_type

    def set_event_type(self, event_type):
        """ Set the event type [ Alarm | Metric ] """
        if event_type is not None:
            self.event_type = event_type

    def set_notify_target(self, target, notify):
        """ Set the notification prefs
            target = [ Slack | PagerDuty | Splunk ]
            notify = bool
        """
        target_attribute = "notify_" + target.lower()
        if hasattr(self, target_attribute):
            self.set_attribute(target_attribute, notify)

    def set_environment(self, env):
        """ Set the event source environment """
        if env is not None:
            self.environment = env

    def set_service(self, service):
        """ Set the resource parent service name eg CSLS """
        if service is not None:
            self.service = service

    def set_healthy(self, healthy):
        """ Set the current health status of the resource
            healthy = bool
        """
        if healthy is not None:
            self.healthy = healthy

    def set_resource(self, resource_name=None, resource_id=None):
        """ Set the resource name and/or id
            Different resources in AWS have
            either no name or no id.
        """
        self.resource = {"Name": resource_name, "ID": resource_id}

    def set_source_data(self, source_data):
        """ Pass the original source event unaltered """
        if source_data is not None:
            self.source_data = source_data

    def set_metric_data(self, metric_data):
        """ Pass the CloudWatch get-metric-statistics data unaltered """
        if metric_data is not None:
            self.metric_data = metric_data

    def to_json(self):
        """ Convert to dict
            Change case from python snake_case to UpperCamelCase
            and convert to JSON
        """
        event_dict = vars(self)
        camel_dict = {}
        for key, val in event_dict.items():
            key_words = key.split("_")
            camel_key = "".join(x.title() for x in key_words)
            camel_dict[camel_key] = val
        event_json = json.dumps(camel_dict, default=str)
        return event_json
