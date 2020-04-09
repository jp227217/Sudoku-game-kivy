import pickle

# to stroe date in file
pickle_out=open('sudoko.txt','wb')
pickle.dump(s,pickle_out)
print("done")
pickle_out.close()

# to rectrive the date from file
pickle_in=open('sudoko.txt','rb')
k=pickle.load(pickle_in)
print(k)
pickle_in.close()