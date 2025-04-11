import pandas as pd
import os
from datetime import datetime
from typing import List, Optional
import sys
import openpyxl
import openpyxl.cell._writer
import openpyxl.worksheet._writer
import openpyxl.workbook
import openpyxl.worksheet._write_only

class ExcelCreator:
    def __init__(self, output_directory="exports"):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        self.output_directory = os.path.join(base_path, output_directory)
        self._ensure_output_directory()

    def _ensure_output_directory(self):
        try:
            os.makedirs(self.output_directory, exist_ok=True)
            test_file = os.path.join(self.output_directory, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except Exception as e:
            print(f"Directory creation/permission error: {str(e)}")
            self.output_directory = os.path.join(os.path.expanduser('~'), 'Documents', 'LinkedInExports')
            os.makedirs(self.output_directory, exist_ok=True)
            print(f"Fallback directory created at: {self.output_directory}")

    def _save_to_excel(self, df: pd.DataFrame, filename: str) -> None:
        try:
            if os.path.exists(filename):
                try:
                    existing_df = pd.read_excel(filename)
                    df = pd.concat([existing_df, df], ignore_index=True)
                except Exception as e:
                    print(f"Error reading existing file: {str(e)}")
                    pass
            
            try:
                df.to_excel(filename, index=False)
                print(f"Successfully saved data to: {filename}")
            except PermissionError:
                base, ext = os.path.splitext(filename)
                new_filename = f"{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                df.to_excel(new_filename, index=False)
                print(f"File saved with new name due to permissions: {new_filename}")
                return
                
        except Exception as e:
            print(f"Error saving Excel file: {str(e)}")
            try:
                fallback_path = os.path.join(os.path.expanduser('~'), 'Documents', 'LinkedInExports')
                os.makedirs(fallback_path, exist_ok=True)
                fallback_file = os.path.join(fallback_path, os.path.basename(filename))
                df.to_excel(fallback_file, index=False)
                print(f"File saved to fallback location: {fallback_file}")
            except Exception as e2:
                raise IOError(f"Failed to save file in both locations: {str(e2)}")

    def _validate_profiles(self, profiles: List) -> None:
        if not profiles:
            raise ValueError("Profile list is empty")

    def _extract_profile_data(self, profile) -> dict:
        try:
            return {
                'Name': profile.name,
                'Title': profile.title,
                'Location': profile.location,
                'Summary': profile.summary,
                'Connections': profile.connections,
                'Profile Link': profile.profile_link
            }
        except AttributeError as e:
            print(f"Missing profile data: {str(e)}")
            return None

    def _create_dataframe(self, profiles: List) -> pd.DataFrame:
        data = {
            'Name': [],
            'Title': [],
            'Location': [],
            'Summary': [],
            'Connections': [],
            'Profile Link': []
        }

        for profile in profiles:
            profile_data = self._extract_profile_data(profile)
            if profile_data:
                for key in data:
                    data[key].append(profile_data[key])

        if not any(data.values()):
            raise ValueError("No data found for export")

        return pd.DataFrame(data)

    def _generate_filename(self, search_term: str) -> str:
        return f"{self.output_directory}/linkedin_profiles_{search_term.replace(' ', '_')}.xlsx"

    def _save_to_excel(self, df: pd.DataFrame, filename: str) -> None:
        try:
            if os.path.exists(filename):
                existing_df = pd.read_excel(filename)
                df = pd.concat([existing_df, df], ignore_index=True)
            df.to_excel(filename, index=False)
        except PermissionError:
            raise PermissionError(f"No permission to create/update Excel file: {filename}")
        except Exception as e:
            raise IOError(f"Error creating/updating Excel file: {str(e)}")

    def export_profiles(self, profiles: List, search_term: str) -> Optional[str]:
        try:
            self._validate_profiles(profiles)
            df = self._create_dataframe(profiles)
            filename = self._generate_filename(search_term)
            self._save_to_excel(df, filename)
            print(f"\n{len(profiles)} profiles exported to: {filename}")
            return filename

        except (ValueError, PermissionError, IOError) as e:
            print(f"Error during export: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None