import re
import matplotlib.pyplot as plt
import ast

def get_lists(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
        y = []
        x = []
        for line in lines:
            if 'eval_loss' in line:
                corrected_line = line.replace('\t','')
                corrected_line = corrected_line.replace(' ', '')
                try:
                    dic = ast.literal_eval(corrected_line)
                    x.append(dic['epoch'])
                    y.append(dic['eval_loss'])
                except:
                    continue
        return x , y

x_bart_new , y_bart_new = get_lists('final_scratch5e-5_5000_warmup.txt')
# x_bart_old , y_bart_old = get_lists('oldbartlr5e-5_2.txt')
# x_t5_new , y_t5_new = get_lists('newlr8e-5.txt')
# x_t5_old , y_t5_old = get_lists('oldlr8e-5_2.txt')
#
# print(y_t5_new)
# print(y_t5_old)
# print(len(x_bart_old))
# print(len(x_bart_new))
# print(len(x_t5_old))
# print(len(x_t5_new))
from matplotlib.pyplot import figure

figure(figsize=(6, 6), dpi=80)

plt.plot(x_bart_new, y_bart_new)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
# plt.title("7 sentences split - Improved Format \n T5 architecture training from scratch - Validation loss (CE)")
plt.show()

# plt.plot(x_bart_new,y_bart_new, label = 'Finetuned-Bart Improved Format')
# plt.plot(x_bart_old[:88],y_bart_old[:88], label = 'Finetuned-Bart Baseline Format')
# plt.plot(x_t5_new,y_t5_new, label = 'Finetuned-T5 Improved Format')
# plt.plot(x_t5_old[:88],y_t5_old[:88], label = 'Finetuned-T5 Baseline Format')
# plt.legend()
# plt.title("10 sentences split \n Finetuned models validation loss (CE)")
# plt.show()

