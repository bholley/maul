from StringSVM import StringSVM

svm = StringSVM()
svm.addSamples([("moz", "Mozilla"),
                ("moz", "Mozila"),
                ("moz", "Muzilla"),
                ("gog", "Chrome"),
                ("gog", "Chrum")])
svm.finalize()
svm.train()
