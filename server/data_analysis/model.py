import torch
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,
    event_level=logging.ERROR
)
sentry_sdk.init(
    dsn="https://de11a1016667481096a0b4fd02346103@o358880.ingest.sentry.io/5450617",
    integrations=[sentry_logging]
)


class AutoEncoder(torch.nn.Module):
    def __init__(self, input_shape):
        super().__init__()
        self.encoder_hidden_layer = torch.nn.Linear(
            in_features=input_shape, out_features=128
        )
        self.encoder_output_layer = torch.nn.Linear(
            in_features=128, out_features=128
        )
        self.decoder_hidden_layer = torch.nn.Linear(
            in_features=128, out_features=128
        )
        self.decoder_output_layer = torch.nn.Linear(
            in_features=128, out_features=input_shape
        )

    def forward(self, x):
        x = self.encoder_hidden_layer(x)
        x = torch.relu(x)
        x = self.encoder_output_layer(x)
        x = torch.relu(x)
        x = self.decoder_hidden_layer(x)
        x = torch.relu(x)
        x = self.decoder_output_layer(x)
        x = torch.relu(x)
        logging.info("Model forward pass complete")
        return x
