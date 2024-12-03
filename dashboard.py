# from text import TextContent
# from code import CodeContent
import streamlit as st
import subprocess
import os

# b0397a76fb2b6b66b20aec7efdd912
# 11b56774af2ce105e788290a0f27e612ecfb7d7c54dd67c23a6cfad9e6875f0d

def run_c_code(code):
    """
    Compiles and runs the given C code, then displays the output or errors.
    :param code: str
    :return:
    """
    # Save the code to a temporary file
    with open("temp.c", "w") as f:
        f.write(code)

    # Compile the C code
    compile_result = subprocess.run(["gcc", "temp.c", "-o", "temp.out"], capture_output=True, text=True)

    if compile_result.returncode != 0:
        # Display compilation errors
        st.error(f"Compilation failed:\n{compile_result.stderr}")
    else:
        # Run the compiled binary
        run_result = subprocess.run(["./temp.out"], capture_output=True, text=True)

        # Display the output or runtime errors
        if run_result.returncode != 0:
            st.error(f"Runtime error:\n{run_result.stderr}")
        else:
            st.text_area("Output:", value=run_result.stdout, height=200)

    # Clean up temporary files
    if os.path.exists("temp.c"):
        os.remove("temp.c")
    if os.path.exists("temp.out"):
        os.remove("temp.out")

class CreateDashboard:
    def __init__(self, topic):
        self.topic = topic
        self.content = {
            "intro": {
                "intro": {
                    "text": "intro.txt",
                    "images": {
                        "arreglo_c.png": None,
                        "arreglos.png": "Ejemplo de un arreglo",
                        "lista-enlazada.jpg": "Ejemplo de lista enlazada",
                        "grafos.png": "Ejemplo de un grafo",
                        "pilas_colas.png": "Ejemplo de pilas y colas",
                        "arbol.png": "Ejemplo de un árbol"
                    },
                    "code": None
                },
            },
            "static_structures": {
                "introduction": {
                    "text": "introduction.txt",
                    "images": {
                        "static_ds.jpg": "Arreglo como ejemplo de una estructura estática",
                    }
                },
                "arrays": {
                    "text": "arrays.txt",
                    "images": {
                        "arreglos.png": "Ejemplo de un arreglo",
                        "2d_arreglos.jpg": "Ejemplo de un arreglo bidimensional"
                    }
                },
                "dynamic_memory": {
                    "text": "dynamic_memory.txt",
                    "images": None
                },
                "queues_using_arrays": {
                    "text": "queues.txt",
                    "images": {
                        "queue_life.jpg": "Cola en la vida real",
                        "cola_estructura.png": "Estructura de una cola"
                    }
                },
                "stacks_using_arrays": {
                    "text": "stacks.txt",
                    "images": {
                        "stack.png": "Ejemplo de una pila",
                        "platos.jpg": "Ejemplo de una pila en la vida real"
                    }
                }
            },
            "dynamic_structures": "",
            "sorting_algorithms": "",
            "searching_algorithms": ""
        }
        self.tabs = {
            "intro": ["Introducción"],
            "static_structures": ["Introducción", "Arreglos", "Asignación de Memoria Dinámica", "Colas", "Stacks"]
        }
        self.image_formats = [".jpg", ".png"]
        self.language_code = "c"

    def display_text(self, data, key):
        """
        This method does something...
        :return:
        """

        name = data["text"]
        path = f"{self.topic}/{key}/text/{name}"
        text_content = open(path, "r", encoding='utf-8').read().split("\n\n")

        for text in text_content:

            if text[-4:] in self.image_formats:
                image_path = f"{self.topic}/{key}/images/{text}"
                left_co, cent_co, last_co = st.columns([0.1, 0.8, 0.1])
                with cent_co:
                    st.image(image_path, data["images"][text])
                continue

            elif text[:4] == "code":
                self.display_code(key, text)
                continue

            # st.markdown(fr"{text}", unsafe_allow_html=True)
            st.markdown(fr"{text}", unsafe_allow_html=True)

    def display_code(self, key, name):
        """
        This method does something...
        :param data:
        :return:
        """
        path = f"{self.topic}/{key}/code/{name}"
        code_content = open(path, "r").read()

        st.markdown("##### Código de Ejemplo")

        # Display the "intro" code
        selected_code = code_content
        st.code(selected_code, language=self.language_code)

        # Button to run the code
        if st.button("Run Code", key=name):
            run_c_code(selected_code)

    def display_dashboard(self):
        """
        This method does something...
        :return:
        """

        data = self.content[self.topic]
        keys = list(data.keys())
        tabs = self.tabs[self.topic]

        shown_tabs = st.tabs(tabs)

        for i in range(len(tabs)):
            with shown_tabs[i]:

                self.display_text(data[keys[i]], keys[i])
