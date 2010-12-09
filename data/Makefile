all: maul.db nastydb

maul.db: uadata_clean_token_finished.txt
	python GenerateDB.py maul.db uadata_clean_token_finished.txt

uadata_clean_token_finished.txt: uadata_clean_token.txt
	python finish_data.py

nastydb:
	python GenerateDB.py nastydb ./source/nasty_ones.txt
	python ExcludeDB.py

uadata_clean_token.txt:
	python tokengen.py

clean:
	rm -f *.txt
	rm -f *~

clobber: clean
	rm -f maul.db
	rm -f nastydb
