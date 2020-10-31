from rest_framework import serializers

class UnitedStatesSerializer(serializers.Serializer):
	video_id = serializers.CharField(required=True, max_length=26)
	channel_title = serializers.CharField(required=False)
	trending_date = serializers.DateField()
	category = serializers.IntegerField()
	tags = serializers.CharField()
	