from transformers import BartConfig, BartForConditionalGeneration

class Bart():
    def __init__(self, tokenizer):
        # super().__init__(config)
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
        return self.shift_tokens_right(labels, self.config.pad_token_id, self.config.decoder_start_token_id)

    def forward(self, sentence, labels):
        input_ids = self.tokenizer.batch_encode_plus(sentence, add_special_tokens=False, return_tensors="pt",
                                          padding=True).input_ids

        if labels is not None:
            labels = self.tokenizer.batch_encode_plus(labels, add_special_tokens=False, return_tensors="pt",
                                                      padding=True).input_ids
            decoder_input_ids = self.prepare_decoder_input_ids_from_labels(labels)

            outputs = self.model(input_ids=input_ids, decoder_input_ids=decoder_input_ids, labels=labels)

        return outputs
