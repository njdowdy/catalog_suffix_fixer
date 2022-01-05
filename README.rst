=================
CATALOG SUFFIX FIXER
=================

HOW TO USE
^^^^^^^^^^
#. Ensure ``python3`` is installed on your system (see: `here <https://www.python.org/downloads/>`_)
#. Install ``poetry`` on your system (see: `here <https://python-poetry.org/docs/#installation>`_)
#. Run from the directory of your choice:
    - ``git clone https://github.com/njdowdy/catalog_suffix_fixer.git``
    - ``cd catalog_suffix_fixer``
    - ``poetry install``
    - ``source`poetry env info --path`/bin/activate``
#. Ensure a folder at ``catalog_suffix_fixer/input`` exists with at least one subdirectory (e.g., ``catalog_suffix_fixer/input/myDept``)
#. Adjust ``script.py`` to reflect the path you want to watch and adjust other options as needed
#. To Run Headless:
    - Linux:
        ``nohup python script.py &``
    - Windows:
        Work in Progress...
#. To close the  virtual environment, run:
    - ``deactivate``

To update the source code:
    #. ``git pull origin``

SET UP AS A LOCAL SERVICE ON BOOT
^^^^^^^^^^
Linux:
    #. Create ``systemd`` file at:
        ``/etc/systemd/system/catalog_suffix_fixer.service``
    #. Save these contents to the .service file:

        [Unit]
        Description=Catalog Suffix Fixer Watchdog

        [Service]
        ExecStart=/path/to/poetry/env/bin/python3 /path/to/file/script.py
        Restart=always

        [Install]
        WantedBy=multi-user.target
    #. ``systemctl daemon-reload``
    #. ``systemctl enable catalog_suffix_fixer.service``

    Controls:
        * Start it: ``systemctl start catalog_suffix_fixer``
        * Restart it: ``systemctl restart catalog_suffix_fixer``
        * Stop it: ``systemctl stop catalog_suffix_fixer``
        * Get the status: ``systemctl status catalog_suffix_fixer``
        * View logs: ``journalctl -u catalog_suffix_fixer``

Windows:
    #. Work in Progress...

CONTACT
^^^^^^^^^^
Please report issues or questions `here <https://github.com/njdowdy/catalog_suffix_fixer/issues>`_.
