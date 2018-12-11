import json
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
	context = { 'debug' : True }

	try:
		assistant = AssistantV1(
			version=cred['version'],
			iam_apikey=cred['apiKey'],
			url=cred['url']
			)

		workspace = cred['workspace_id']

		while True:
			input_message = input("Ask the chatbot (e.g. I want to order pizza): ")

			response = assistant.message(
				workspace_id=workspace,
				input={'text' : input_message},
				context=context
				).get_result()

			print(json.dumps(response, indent=2))
			print("Bot response: ", response['output']['text'][0])
			print('\n\n\n')

			context = response['context']

	except WatsonException as wex:
		print("Watson Error: ", wex)
		sys.exit()
	except KeyError as missingKey:
		print("% key is missing in credentials" % missingKey)
		sys.exit()


if __name__ == '__main__':
    main()