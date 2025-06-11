printf "\
mkdir -p ~/.streamlit/\n\
echo \"[server]\n\
headless = true\n\
enableCORS=false\n\
port = \$PORT\n\
\" > ~/.streamlit/config.toml
" > setup.sh

chmod +x setup.sh
