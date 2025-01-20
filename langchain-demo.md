# Run
### Import all relevant packages
```
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.runnables import RunnableParallel
```
### Move to the llama.cpp directory
**Shell**
```
cd llama.cpp
```
**Jupyter Notebook**
```
!cd llama.cpp
```

### Setup callback manager
```
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
```

#### Load the models
```
n_gpu_layers = -1
n_batch = 4096
n_ctx = 4096
max_tokens = 100

LLM1 = LlamaCpp(
        model_path="models/Llama-3.2-3B-Instruct-Q5_K_M.gguf",
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        n_ctx=n_ctx,
        max_tokens=max_tokens,
        f16_kv=True,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
        )

LLM2 = LlamaCpp(
        model_path="models/Llama-3.2-3B-Instruct-Q5_K_M.gguf",
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        n_ctx=n_ctx,
        max_tokens=max_tokens,
        f16_kv=True,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
        )
```
### Setup the templates
```
template1 =  """
    You are a medical expert. Below is a clinical note for a patient.
    
    Clinical Note:
    {clinical_note}
    
    Based on the clinical note, provide the most likely primary diagnosis only. Do not include additional text.
"""

prompt1 = PromptTemplate(template=template1, input_variables=['clinical_note'])

template2 =  """
    You are a medical consultant. Please review the following clinical note and original primary diagnosis from a medical expert.
    
    Clinical Note:
    {clinical_note}

    Original Primary Diagnosis:
    {prim_dx}
    
    Write one sentence stating whether agree or disagree with the original primary diagnosis and provide some reasoning.
"""

prompt2 = PromptTemplate(template=template2, input_variables=['clinical_note','prim_dx'])

template3 =  """
    Below is a clinical note, and your primary diagnosis based on the clinical note.
    
    Clinical Note:
    {clinical_note}
    
    Your Primary Diagnosis:
    {prim_dx}

    A second medical consultant was brought in to evaluate your primary diagnosis based on the clinical note. The medical consultant was asked whether
    they agree or disagree with your primary diagnosis. Here is their response:
    
    Response from consultant:
    {response}

    Based on the response from the medical consultant, would you like to change your primary diagnosis? Please provide a one sentence response.
"""

prompt3 = PromptTemplate(template=template3, input_variables=['clinical_note','prim_dx','response'])
```

### Chain the prompts to the LLMs
```
llm_chain1 = prompt1 | LLM1
llm_chain2 = prompt2 | LLM2
llm_chain3 = prompt3 | LLM1
```

### Create the overall chain
```
overall_chain = (
    # Step 1: Produce "prim_dx" by calling chain1 with {"clinical_note": x["clinical_note"]}.
    RunnableParallel({
        # Keep the original clinical_note around
        "clinical_note": lambda x: x["clinical_note"],
        # Call chain1 with the prompt it needs
        "prim_dx": lambda x: llm_chain1.invoke({"clinical_note": x["clinical_note"]})
    })
    # Step 2: Produce "response" by calling chain2 with both "clinical_note" and "prim_dx"
    | RunnableParallel({
        "clinical_note": lambda x: x["clinical_note"],
        "prim_dx": lambda x: x["prim_dx"],
        "response": lambda x: llm_chain2.invoke({
            "clinical_note": x["clinical_note"],
            "prim_dx": x["prim_dx"]
        })
    })
    # Step 3: Now the dictionary contains {"clinical_note", "prim_dx", "response"}, 
    # which is exactly what chain3 needs.
    | llm_chain3
)
```

