This is a simple python script that helps you to create Announcer Quotes pages for the [Heroes of the Storm Gamepedia](https://heroesofthestorm.gamepedia.com/).
### Syntax
`python announcer.py <quotes_file> <query_string> [output_file]
### Parameters
- `quotes_file` - a `ConversationStrings.txt` file from the game files that contains the quotes for the required announcer.
- `query_string` - a query string to filter out the quotes for the required announcer. Case sensitive. Example: to filter out Alarak's quotes which have syntax like `VoiceOver/AlarakA/EndingLose03=You have considerably more to learn.` you will have to use `AlarakA` query string.
- `output_file` - optional parameter. A file where the output wiki code will be placed. If not specified, it will be based on the query string.
