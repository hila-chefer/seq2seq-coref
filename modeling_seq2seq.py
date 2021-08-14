from transformers import BartConfig, BartForConditionalGeneration, BartModel
from torch.nn import Module

class Bart(Module):
    def __init__(self, tokenizer):
        super().__init__()
        self.config = BartConfig()
        self.model = BartForConditionalGeneration(self.config)
        self.tokenizer = tokenizer

    def shift_tokens_right(self, input_ids, pad_token_id, decoder_start_token_id):
        """
        Shift input ids one token to the right.
        """
        shifted_input_ids = input_ids.new_zeros(input_ids.shape)
        shifted_input_ids[:, 1:] = input_ids[:, :-1].clone()
        shifted_input_ids[:, 0] = decoder_start_token_id

        assert pad_token_id is not None, "self.model.config.pad_token_id has to be defined."
        # replace possible -100 values in labels by `pad_token_id`
        shifted_input_ids.masked_fill_(shifted_input_ids == -100, pad_token_id)

        return shifted_input_ids

    def prepare_decoder_input_ids_from_labels(self, labels):
        return self.shift_tokens_right(labels, self.config.pad_token_id, 2)

    def forward(self, input_ids, decoder_input_ids, labels=None, attention_mask=None):

        outputs = tuple()
        if labels is not None:
            losses = {}

            loss = self.model(attention_mask=attention_mask.to(self.model.device),
                                 input_ids=input_ids.to(self.model.device),
                                 decoder_input_ids=decoder_input_ids.to(self.model.device),
                                 labels=labels.to(self.model.device))[0]

            losses.update({"loss": loss})
            outputs = (loss,) + outputs + (losses,)

        return outputs
