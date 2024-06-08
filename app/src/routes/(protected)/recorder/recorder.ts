export type Prompt = {
	id: string;
	index: number;
	content: string;
};

export type PromptResponse = Prompt & {
	recordings: { blob: Blob; note: string }[];
};

/**
 * Mostly transforms the `Reader` API into a promise-based API.
 */
export function readAsPlaintext(file: File): Promise<string> {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.onload = () => resolve(reader.result as string);
		reader.onerror = reject;
		reader.readAsText(file);
	});
}

export function parsePromptFile(promptFile: string): Prompt[] {
	return promptFile
		.trim()
		.split(/\r?\n/)
		.map((line, index) => {
			const [id, ...prompt] = line.split(' ');

			return {
				id,
				index,
				content: prompt.join(' ')
			};
		});
}
