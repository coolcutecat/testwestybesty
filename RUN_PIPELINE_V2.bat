@echo off
echo ================================
echo FULL PIPELINE v2.0 - TEST
echo ================================
echo.
echo Running complete automation prep...
echo.

cd C:\Collin\Collinism\Claude\manhwa_pipeline
python run_full_pipeline.py

echo.
echo ================================
echo Prep complete!
echo.
echo Next: Open Premiere and run the 3 JSX scripts
echo.
pause
