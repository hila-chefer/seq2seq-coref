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

x_bart_new , y_bart_new = get_lists('newbartlr1e-5.txt')
x_bart_old , y_bart_old = get_lists('oldbartlr5e-5_2.txt')
x_t5_new , y_t5_new = get_lists('newlr8e-5.txt')
x_t5_old , y_t5_old = get_lists('oldlr8e-5_2.txt')


from matplotlib.pyplot import figure

figure(figsize=(6, 6), dpi=80)
plt.plot(x_bart_new,y_bart_new, label = 'Finetuned-Bart Our format')
plt.plot(x_bart_old[:88],y_bart_old[:88], label = 'Finetuned-Bart Baseline format')
plt.plot(x_t5_new,y_t5_new, label = 'Finetuned-T5 Our format')
plt.plot(x_t5_old[:88],y_t5_old[:88], label = 'Finetuned-T5 Baseline format')
plt.legend(fontsize=17)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()

