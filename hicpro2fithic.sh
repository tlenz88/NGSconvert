for i in $(ls ${1}/*/*.matrix | rev | cut -c 8- | rev | uniq); do
	SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
	OUTDIR=$(cd $(dirname $i) && pwd)
	ORGDIR="/mnt/f/organism_genome/Pfalciparum3D7"
	if [[ $i != *iced* ]] && [[ $i != *normalized* ]] && [[ $i != *cpm* ]]; then
		RESOLUTION=$(head -1 ${i}_abs.bed | awk '{print $3 - $2}')
		python3 $SCRIPT_DIR/HiC-Pro/bin/utils/hicpro2fithic.py -i ${i}.matrix -b ${i}_abs.bed -s ${i}_iced.matrix.biases -o $OUTDIR -r $RESOLUTION
		fithic -f $OUTDIR/fithic.fragmentMappability.gz -i $OUTDIR/fithic.interactionCounts.gz -o $OUTDIR -r $RESOLUTION -t $OUTDIR/fithic.biases.gz
		python3 $SCRIPT_DIR/plot_fithic.py $ORGDIR/PlasmoDB-58_Pfalciparum3D7_Genome.chrom.sizes $ORGDIR/Pfalciparum3D7_centromeres.txt $ORGDIR/var_genes.gff $OUTDIR/FitHiC.spline_pass1.res10000.significances.txt.gz
	fi
done
