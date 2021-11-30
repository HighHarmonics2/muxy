from rest_framework import serializers

from events.models import Event, EventStreamURL, Stream


class EventStreamURLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventStreamURL
        fields = ("url", "name")


class EventSerializer(serializers.HyperlinkedModelSerializer):
    stream_urls = EventStreamURLSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"

    def validate(self, attrs):
        starts_at = attrs.get("starts_at")
        ends_at = attrs.get("ends_at")

        if starts_at and ends_at:
            if ends_at < self.starts_at:
                raise serializers.ValidationError("event ends before starting")

            preparation_time = attrs.get("preparation_time")
            duration_in_minutes = (ends_at - starts_at).total_seconds() // 60
            if preparation_time and preparation_time > duration_in_minutes:
                raise serializers.ValidationError(
                    "preparation time (%d) is longer than the duration of the event (%d)"
                    % (preparation_time, duration_in_minutes)
                )

        return attrs


class StreamSerializer(serializers.HyperlinkedModelSerializer):
    recordings = serializers.SerializerMethodField()

    class Meta:
        model = Stream
        fields = (
            "url",
            "publisher_name",
            "publisher_email",
            "description",
            "location",
            "timezone",
            "starts_at",
            "ends_at",
            "key",
            "live_at",
            "event",
            "recordings",
        )

    def get_recordings(self, stream):
        request = self.context.get("request")
        return [request.build_absolute_uri(path) for path in stream.recording_paths]

    def validate(self, attrs):
        starts_at = attrs.get("starts_at")
        ends_at = attrs.get("ends_at")
        key = attrs.get("key")

        if starts_at and ends_at:
            other_streams = Stream.objects.filter(
                event=attrs["event"],
                starts_at__lt=attrs["ends_at"],
                ends_at__gt=attrs["starts_at"],
            )
            if key:
                other_streams = other_streams.exclude(key=attrs["key"])
            if other_streams.exists():
                events_str = [str(s) for s in other_streams.all()]
                raise serializers.ValidationError(
                    "overlaps with other streams: %s" % events_str
                )

        return attrs
