
To translate a Cisco topology to FRR run:

```bash
python cisco_translator -t <topo-name>
```

* `sed -i '/100/d' links.txt`
* `find . -type f -name "*.cfg" | xargs sed -i '/ip ospf cost/c\ ip ospf cost 1'`