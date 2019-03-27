#!/bin/bash

ssh -T -p 14501 "osboxes@localhost" << 'EOF'
    echo "Getting Internal IP"
    echo ls
EOF