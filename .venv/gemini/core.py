import json
import google.generativeai as genai
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class GeminiChat:

    def __init__(
        self, gemini_token: str, image=None, chat_history: list = None
    ) -> None:
        self.image = image
        self.chat_history = chat_history
        self.GOOGLE_API_KEY = gemini_token

        genai.configure(api_key=self.GOOGLE_API_KEY)

        with open("safety_settings.json", "r") as fp:
            self.safety_settings = json.load(fp)

        logging.info("Initiated new chat model")

    def _handle_exception(self, operation: str, e: Exception) -> None:
        logging.warning(f"Failed to {operation}: {e}")
        raise ValueError(f"Failed to {operation}: {e}")

    def _get_model(self, generative_model: str = "gemini-2.0-flash") -> genai.GenerativeModel:
        # модель
        try:
            logging.info("Trying to get generative model")
            return genai.GenerativeModel(
                generative_model, safety_settings=self.safety_settings
            )
        except Exception as e:
            self._handle_exception("get model", e)

    def send_image(self, message_text: str | None = None) -> str:
        message_text = message_text or "Please describe this photo"
        try:
            model = self._get_model("gemini-2.0-flash")
            response = model.generate_content([message_text, self.image], stream=True)
            response.resolve()
            logging.info("Recieved response from Gemini")
            return "".join([text for text in response.text])
        except Exception as e:
            self._handle_exception("send image", e)
            return "Не можем подключиться к серверам Google. Попробуйте ещё раз..."

    def start_chat(self) -> None:
        # Начало новой сессии
        try:
            model = self._get_model()
            self.chat = model.start_chat(history=self.chat_history)
            logging.info("Start new conversation")
        except Exception as e:
            self._handle_exception("start chat", e)

    def send_message(self, message_text: str) -> str:
        try:
            response = self.chat.send_message(message_text, stream=True)
            response.resolve()
            logging.info("Recieved response from Gemini")
            return "".join([text for text in response.text])
        except Exception as e:
            self._handle_exception("send message", e)
            return "Не можем подключиться к серверам Google. Попробуйте ещё раз..."

    def get_chat_title(self) -> str:
        try:
            return self.send_message(
                "Write a one-line short title up to 10 words for this conversation in plain text."
            )
        except Exception as e:
            self._handle_exception("get chat title", e)

    def get_chat_history(self):
        try:
            return self.chat.history
        except Exception as e:
            self._handle_exception("get chat history", e)

    def close(self) -> None:
        logging.info("Closed model instance")
        self.chat = None
        self.chat_history = []
