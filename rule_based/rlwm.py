rules=[['animal-check',
			[['cellwall','?organism','no']],
			[['animal','?organism']]],
		['plant-check',
			[['chlo','?organism','has']],
			[['plant','?organism']]],
		['bird-check',
			[['animal','?organism'],['feather','?organism','has']],
			[['bird','?organism']]],
		['mammal-check',
			[['feather','?organism','no'],['warm','?organism'],['animal','?organism']],
			[['mammal','?organism']]],
		['wing-check',
			[['bird','?organism']],
			[['wing','?organism']]],
		['bat-check',
			[['wing','?organism'],['mammal','?organism']],
			[['bat','?organism']]],
		['penguin-check',
			[['fly','?organism','not'],['bird','?organism'],['live','?organism','Antarctic']],
			[['penguin','?organism']]],
		['spermatophyte-check',
			[['plant','?organism'],['seed','?organism']],
			[['spermatophyte','?organism']]],
		['flowering-check',
			[['spermatophyte','?organism'],['flowering','?organism']],
			[['floweringplant','?organism']]],
		['swim-check',
			[['penguin','?organism']],
			[['swim','?organism','can']]]]


wm=[
	['cellwall','human','no'],
	['feather','human','no'],
	['warm','human'],
	['animal','kingpenguin'],
	['feather','kingpenguin','has'],
	['fly','kingpenguin','not'],
	['live','kingpenguin','Antarctic'],
	['chlo','rose','has']]

