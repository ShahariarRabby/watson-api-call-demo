import json
import os
import sys
from watson_developer_cloud import AuthorizationV1, AssistantV1, WatsonException


def get_credential_data() :
	credential_file = "credential.json"

	try:
		with open(credential_file, 'r') as cf:
			cred = json.load(cf)

		return cred
	except FileNotFoundError:
		print("Error!", "Cannot find credential file")
		sys.exit(0)
	except Exception:
		print("Error!", "Failed to read credential file")
		sys.exit(0)


def main() :
	print("---\nThis is a demo bot for making Watson Assistant API calls\n---\n")

	cred = get_credential_data()

	try:
		assistant = AssistantV1(
			version=cred['version'],
			iam_apikey=cred['apiKey'],
			url=cred['url']
			)

		input_message = raw_input("Ask the chatbot (e.g. I want to order pizza): ")

		workspace = cred['workspace_id']

		response = assistant.message(
			workspace_id=workspace,
			input={'text' : input_message}
			).get_result()

		print(json.dumps(response, indent=2))
		print("Bot response: ", response['output']['text'][0])

	except WatsonException as wex:
		print wex
		sys.exit(0)
	except KeyError as missingKey:
		print "% key is missing in credentials" % missingKey
		sys.exit(1)


if __name__ == '__main__':
    main()