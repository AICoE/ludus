ENV_FILE := .env
include ${ENV_FILE}
export $(shell sed 's/=.*//' ${ENV_FILE})

deploy_ultrahook:
	oc process -f openshift/ludus.ultrahook.deployment.template.yaml \
		--param ULTRAHOOK_API_KEY=`echo "${ULTRAHOOK_API_KEY}" | base64` \
		--param ULTRAHOOK_SUBDOMAIN=${ULTRAHOOK_SUBDOMAIN} \
		--param ULTRAHOOK_DESTINATION=${ULTRAHOOK_DESTINATION} | oc apply -f -

delete_ultrahook:
	oc process -f openshift/ludus.ultrahook.deployment.template.yaml \
		--param ULTRAHOOK_API_KEY=`echo "${ULTRAHOOK_API_KEY}" | base64` \
		--param ULTRAHOOK_SUBDOMAIN=${ULTRAHOOK_SUBDOMAIN} \
		--param ULTRAHOOK_DESTINATION=${ULTRAHOOK_DESTINATION} | oc delete -f -

deploy_event_listener:
	oc process -f openshift/ludus.event_listener.deployment.template.yaml \
		--param GITHUB_URL=${GITHUB_URL} \
		--param KAFKA_TOPIC=${KAFKA_TOPIC} \
		--param KAFKA_BOOTSTRAP_SERVER=${KAFKA_BOOTSTRAP_SERVER} | oc apply -f -

delete_event_listener:
	oc process -f openshift/ludus.event_listener.deployment.template.yaml \
		--param GITHUB_URL=${GITHUB_URL} \
		--param KAFKA_TOPIC=${KAFKA_TOPIC} \
		--param KAFKA_BOOTSTRAP_SERVER=${KAFKA_BOOTSTRAP_SERVER} | oc delete -f -

deploy_awarder:
	oc process -f openshift/ludus.awarder.deployment.template.yaml \
		--param GITHUB_URL=${GITHUB_URL} \
		--param KAFKA_TOPIC=${KAFKA_TOPIC} \
		--param KAFKA_BOOTSTRAP_SERVER=${KAFKA_BOOTSTRAP_SERVER} \
		--param AWARDER_NAME=${AWARDER_NAME} \
		--param AWARDER_PORT=${AWARDER_PORT} \
		--param EVENTS_TABLE_NAME=${EVENTS_TABLE_NAME} \
		--param BADGES_TABLE_NAME=${BADGES_TABLE_NAME} | oc apply -f -

delete_awarder:
	oc process -f openshift/ludus.awarder.deployment.template.yaml \
		--param GITHUB_URL=${GITHUB_URL} \
		--param KAFKA_TOPIC=${KAFKA_TOPIC} \
		--param KAFKA_BOOTSTRAP_SERVER=${KAFKA_BOOTSTRAP_SERVER} \
		--param AWARDER_NAME=${AWARDER_NAME} \
		--param AWARDER_PORT=${AWARDER_PORT} \
		--param EVENTS_TABLE_NAME=${EVENTS_TABLE_NAME} \
		--param BADGES_TABLE_NAME=${BADGES_TABLE_NAME} | oc delete -f -
