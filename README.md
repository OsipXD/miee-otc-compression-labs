# miee-otc-compression-labs

### file structure (compression's algorithm independent)

info | bytes
--- | ---
`signature` | `2E 43 45 59 4D`  (`.CEYM` in ASCII)
`name_len` | 1 byte integer
`name` | depends on `name_length` (utf-8 text)
`data` | depends on compression algorithm (see below)

### lab4 (shannon-fano)

`data` сonsists of `frequency table header`, `frequency table chunks` and `data chunks`

#### frequency table header structure

info | bytes
--- | ---
`freq_table_len` | 1 byte integer
`freq_table_chunks` | see `freq_table_lenght` (stucture below)
`data_chunks` | (stucture below)

#### frequency table chunk stucture 

info | bytes
--- | ---
`byte` | 1 byte integer
`n_significant_bits` | 1 byte integer
`significant_bits` | see `n_significant_bits`

#### data chunk stucture

info | bytes
--- | ---
`chunk_bit_len` | 1 byte integer
`data` | see `chunk_bit_len`
