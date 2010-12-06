maul.db: uadata_clean_token_finished.txt
	python GenerateDB.py maul.db uadata_clean_token_finished.txt

uadata_clean_token_finished.txt: uadata_clean_token.txt
	python finish_data.py

uadata_clean_token.txt:
	python tokengen.py

clean:
	rm -f *.txt
	rm -f *~

clobber: clean
	rm -f maul.db
