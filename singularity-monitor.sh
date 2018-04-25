#!/bin/sh

NEW_RELIC_CONFIG_FILE="/app/newrelic.ini"

newrelic-admin generate-config "${NEW_RELIC_LICENSE_KEY}" \
    "${NEW_RELIC_CONFIG_FILE}" || (echo "Error newrelic-admin" && exit 1)

# Application name
sed -i.orig "s,^app_name = \(.*\)$,app_name = ${NEW_RELIC_APP_NAME}," \
	"${NEW_RELIC_CONFIG_FILE}"

# Distributed tracing enabled
sed -i "s,^distributed_tracing.enabled = false,distributed_tracing.enabled = true," \
	"${NEW_RELIC_CONFIG_FILE}"

NEW_RELIC_ENVIRONMENT=${NEW_RELIC_ENVIRONMENT} \
	newrelic-admin run-program "$(command -v singularity-monitor)"
