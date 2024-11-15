from openai import OpenAI
from time import sleep
import uuid

class OpenAIBot:
    def __init__(self, openai_key, assistant_id):
        self.client = OpenAI(api_key=str(openai_key))
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=str(assistant_id))

    # def get_response(self, message):
    #     #step 1: create a thread
    #     thread_id = self.start_conversation()
    #     #step 2: create a message in the thread
    #     self.create_message(thread_id, message)
    #     #step 3: run the assistant
    #     self.run_assistant(thread_id)
    #     #step 4: get the response
    #     response = self.collect_response(thread_id)
    #     return response

    # def delete_users(self):
    #     if self.users:
    #         for user in self.users:
    #             if len(self.users[user]) == 2:
    #                 if (datetime.utcnow() - datetime.fromisoformat(self.users[user][-1])).total_seconds() > 60 * 60:
    #                     del self.users[user]
    #                     print('deleted user')
    #             else:
    #                 print('User did not send the first message yet.')
    #
    #     else:
    #         print('nessun utente')

    def start_conversation(self):
        thread = self.client.beta.threads.create()
        return thread.id

    def create_message(self, thread_id, message):
        try:
            message = self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message,
            )
        except Exception as e:
            print('Exception in create_message: ', e)

    def create_run(self, thread_id):
        # additional_info = f'If required, use these additional informations ' \
        #                   f'of the apartment the guest is in.' \
        #                   f'wifi password: {user_info["wifi_pass"]}, ' \
        #                   f'address: {user_info["address"]}, ' \
        #                   f'pool price: {user_info["pool_price"]}, ' \
        #                   f'price per: {user_info["price_per"]}' \
        #                   f'breakfast: {user_info["breakfast"]}'
        try:
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id, assistant_id=self.assistant.id,
            )
            return run
        except Exception as e:
            print('Exception in create_assistant: ', e)
            exit(2)

    def wait_for_run(self, thread_id, run):
        try:
            while run.status != "requires_action" and run.status != "completed":
                # print(run.status)

                if run.status == 'failed':
                    return run, True

                sleep(0.5)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id,
                )

            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
            return run, False
        except Exception as e:
            print('Exception in wait_for_run: ', e)
            exit(3)

    def collect_response(self, thread_id):
        thread_messages = self.client.beta.threads.messages.list(thread_id=thread_id, order="desc")
        answer = thread_messages.data[0].content[0].text.value
        return answer

    def send_funct_output(self, run, thread_id, call_id, funct_output):
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": call_id,
                    "output": funct_output,
                }
            ]
        )
        return run

    def speech_to_text(self, audio_file):
        try:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"

            )
            return transcript
        except Exception as e:
            print('Exception in transcript_audio: ', e)
            exit(4)

    def text_to_speech(self, text):
        try:
            audio = self.client.audio.speech.create(
                model="tts-1-hd",
                voice="echo",
                input=f"{text}",
                response_format="mp3"
            )
            speech_file_path = f"./static/tmp_audio/{str(uuid.uuid4())}.mp3"
            audio.stream_to_file(speech_file_path)

            return speech_file_path
        except Exception as e:
            print('Exception in text_to_speech: ', e)
            exit(5)
