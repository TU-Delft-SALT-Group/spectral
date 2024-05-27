<script lang="ts">
	import type { mode } from '..';

	export let computedData: mode.ComputedData<'error-rate'>;
	export let fileState: mode.FileState<'error-rate'>;
</script>

<div>
	{#if computedData !== null}
		<div>
			<h2>name: {fileState.name}</h2>
			<h2>id: {fileState.id}</h2>
			<h2>ground truth: {computedData.groundTruth}</h2>
			<div>
				{#each computedData.errorRates as errorRate}
					<h2>word level</h2>
					<h3>wer: {errorRate.wordLevel.wer}</h3>
					<h3>mer: {errorRate.wordLevel.mer}</h3>
					<h3>wil: {errorRate.wordLevel.wil}</h3>
					<h3>wip: {errorRate.wordLevel.wip}</h3>
					<h3>hits: {errorRate.wordLevel.hits}</h3>
					<h3>substitutions: {errorRate.wordLevel.substitutions}</h3>
					<h3>deletions: {errorRate.wordLevel.deletions}</h3>
					{#each errorRate.wordLevel.alignments as alignment}
						{#if alignment.type === 'equal'}
							<span
								>{errorRate.wordLevel.reference
									.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
						{:else if alignment.type === 'deletion'}
							<span style="color:red"
								>{errorRate.wordLevel.reference
									.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
						{:else if alignment.type === 'insert'}
							<span style="color:green"
								>{errorRate.wordLevel.hypothesis
									.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
						{:else if alignment.type === 'substitute'}
							<span style="color:yellow"
								>{errorRate.wordLevel.reference
									.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
							<span style="color:yellowgreen"
								>{errorRate.wordLevel.hypothesis
									.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
						{/if}
					{/each}

					<h2>character level</h2>
					<h3>cer: {errorRate.characterLevel.cer}</h3>
					<h3>substitutions: {errorRate.characterLevel.substitutions}</h3>
					<h3>deletions: {errorRate.characterLevel.deletions}</h3>
					{#each errorRate.characterLevel.alignments as alignment}
						{#if alignment.type === 'equal'}
							<span
								>{errorRate.characterLevel.reference
									.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
						{:else if alignment.type === 'deletion'}
							<span style="color:red"
								>{errorRate.characterLevel.reference
									.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
						{:else if alignment.type === 'insert'}
							<span style="color:green"
								>{errorRate.characterLevel.hypothesis
									.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
						{:else if alignment.type === 'substitute'}
							<span style="color:yellow"
								>{errorRate.characterLevel.reference
									.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
							<span style="color:yellowgreen"
								>{errorRate.characterLevel.hypothesis
									.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
									.reduce((acc, cur) => acc + ' ' + cur, '')}
							</span>
						{/if}
					{/each}
				{/each}
			</div>
		</div>
	{/if}
</div>
