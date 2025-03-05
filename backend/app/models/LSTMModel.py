# models/LSTMModel.py
import torch
import torch.nn as nn
import random

class LSTMSeq2Seq(nn.Module):
    # Define model architecture here, same as you defined in the training code
    def __init__(self, vocab_size, embed_size, hidden_size, embedding_matrix, dropout=0.3):
        super(LSTMSeq2Seq, self).__init__()
        self.embedding = nn.Embedding.from_pretrained(embedding_matrix, freeze=False)
        self.encoder = nn.LSTM(input_size=embed_size, hidden_size=hidden_size, num_layers=1, dropout=0)
        self.decoder = nn.LSTM(input_size=embed_size, hidden_size=hidden_size, num_layers=1, dropout=0)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, src, tgt, teacher_forcing_ratio=0.5):
        embed_src = self.embedding(src)
        embed_tgt = self.embedding(tgt)

        _, (hidden, cell) = self.encoder(embed_src)

        outputs = []
        decoder_input = embed_tgt[:, 0].unsqueeze(1)  # Start token

        for t in range(tgt.shape[1] - 1):  # Ensure same length as target
            output, (hidden, cell) = self.decoder(decoder_input, (hidden, cell))
            output = self.fc(output)
            outputs.append(output)

            # Teacher forcing: Use true target word some of the time
            if random.random() < teacher_forcing_ratio:
                decoder_input = self.embedding(tgt[:, t + 1]).unsqueeze(1)
            else:
                decoder_input = self.embedding(torch.argmax(output, dim=-1)).detach()

        return torch.cat(outputs, dim=1)