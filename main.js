const { createApp, ref, computed, onMounted, watch, nextTick } = Vue;

const app = createApp({
    setup() {
        const textMessage = ref('');
        const messageHtml = ref('');
        const loading = ref(false);
        const errorMessage = ref(null);
        const previewHtml = ref('');

        const convertToHtml = async () => {
            loading.value = true;
            errorMessage.value = null;
            try {
                const response = await axios.post('http://127.0.0.1:5000/convert', { text: textMessage.value });
                messageHtml.value = response.data.html;
                previewHtml.value = response.data.html; // Still set previewHtml
            } catch (error) {
                errorMessage.value = "Error converting text. Please check the backend logs.";
                console.error("Error calling backend:", error);
            } finally {
                loading.value = false;
            }
        };

        onMounted(() => {
            watch(previewHtml, () => {
                nextTick(() => {
                    const iframe = document.getElementById('preview-iframe');
                    if (iframe) {
                        iframe.onload = () => { // Use onload event
                            adjustIframeHeight(iframe);
                        };
                        //initial load
                        adjustIframeHeight(iframe);
                    }
                });
            });
        });

        const adjustIframeHeight = (iframe) => {
            if (iframe && iframe.contentDocument && iframe.contentDocument.body) {
                iframe.style.height = iframe.contentDocument.body.scrollHeight + 'px';
            } else {
                iframe.style.height = '100px';
            }
        }

        return {
            textMessage,
            messageHtml,
            previewHtml,
            convertToHtml,
            loading,
            errorMessage
        };
    },
    template: `
        <div class="container">
            <h1>HTML Previewer</h1>

            <div class="text-to-html">
                <h2>Text to HTML:</h2>
                <textarea v-model="textMessage" placeholder="Enter text message here..." class="input-area"></textarea>
                <button @click="convertToHtml" class="convert-button" :disabled="loading">
                    <span v-if="loading">Loading...</span>
                    <span v-else>Convert to HTML</span>
                </button>
                <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
                <textarea readonly v-model="messageHtml" placeholder="Converted HTML will appear here..." class="output-area"></textarea>
            </div>

            <div class="preview-container">
                <h2>Preview:</h2>
                <iframe id="preview-iframe" :srcdoc="previewHtml" class="preview-area"></iframe>
            </div>
        </div>
    `
});

app.mount('#app');