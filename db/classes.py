import weaviate.classes as wvc
# BELOW WAS PRELIMINARY TEST AND NEEDS UPDATING IF DB IS TO BE UTILISED
weav_classes = {
    "classes": [
        {
            "class": "Submission",
            "description": "Submission Document",
            "vectorizer_config": wvc.config.Configure.Vectorizer.none(),
            "properties": [
                wvc.config.Property(
                    data_type=wvc.config.DataType.TEXT,
                    name="submitter",
                    description="The author of the submission",
                    skip_vectorization=True,
                ),
                wvc.config.Property(
                    name="substantive_submission",
                    data_type=wvc.config.DataType.BOOL,
                    description="Does the submission provide a substantive response to the consultation",
                    skip_vectorization=True,
                ),                
                wvc.config.Property(
                    name="group",
                    data_type=wvc.config.DataType.TEXT,
                    description="Category of the responder",
                    skip_vectorization=True,
                ),
                wvc.config.Property(
                    name="support",
                    data_type=wvc.config.DataType.TEXT,
                    description="Does the responder support the consultation",
                    skip_vectorization=True,
                ),   
                wvc.config.Property(
                    name="support_evidence",
                    data_type=wvc.config.DataType.TEXT,
                    description="Evidence from the consultation",
                    skip_vectorization=True,
                ),                 
                 wvc.config.Property(
                    name="motivations",
                    data_type=wvc.config.DataType.TEXT_ARRAY,
                    description= "Top 3 motivations for the submission.",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="regulation_type",
                    data_type=wvc.config.DataType.TEXT,
                    description= "Does this submission make any comment on the form of regulation provided?",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="regulation_type_evidence",
                    data_type=wvc.config.DataType.TEXT,
                    description= "Does this submission make any comment on the form of regulation provided?",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="regulator_trust",
                    data_type=wvc.config.DataType.TEXT,
                    description= "Does this submission make any comment on the form of regulation provided?",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="regulator_trust_evidence",
                    data_type=wvc.config.DataType.TEXT,
                    description= "Does this submission make any comment on the form of regulation provided?",
                    skip_vectorization=True,
                 ),
                  wvc.config.Property(
                    name="definitions",
                    data_type=wvc.config.DataType.OBJECT_ARRAY,                    
                    description= "Does this submission make any comment on the definitions?",
                    skip_vectorization=True,
                    nested_properties=[
                        wvc.config.Property(
                            name="definition",
                            data_type=wvc.config.DataType.TEXT,                            
                            skip_vectorization=True,
                        ), 
                        wvc.config.Property(
                            name="evidence",
                            data_type=wvc.config.DataType.TEXT,
                            skip_vectorization=True,
                        ),
                    ]
                 ),
                 wvc.config.Property(
                    name="step_2",
                    data_type=wvc.config.DataType.TEXT,                    
                    description= "Does this submission make any comment on the definitions?",
                    skip_vectorization=True,
                    ),
                 wvc.config.Property(
                    name="metadata",
                    data_type=wvc.config.DataType.OBJECT,
                    skip_vectorization=True,
                    nested_properties=[
                       wvc.config.Property(
                            name="groupDefinedBy",
                            data_type=wvc.config.DataType.TEXT,                            
                            skip_vectorization=True,
                        ),
                        wvc.config.Property(
                            name="removed",
                            data_type=wvc.config.DataType.TEXT,                            
                            skip_vectorization=True,
                        ), 
                        wvc.config.Property(
                            name="comments",
                            data_type=wvc.config.DataType.TEXT,                            
                            skip_vectorization=True,
                        ),
                        wvc.config.Property(
                            name="text_extraction_method",
                            data_type=wvc.config.DataType.TEXT,                            
                            skip_vectorization=True,
                        ),
                        wvc.config.Property(
                            name="SUBMISSION_CONTENT",
                            data_type=wvc.config.DataType.TEXT,                            
                            skip_vectorization=True,
                        ),
                        wvc.config.Property(
                            name="step_1",
                            data_type=wvc.config.DataType.OBJECT,                            
                            skip_vectorization=True,
                            nested_properties=[
                                wvc.config.Property(
                                    name="batch_file",
                                    data_type=wvc.config.DataType.TEXT,                            
                                    skip_vectorization=True,
                                ),
                                wvc.config.Property(
                                    name="system_fingerprint",
                                    data_type=wvc.config.DataType.TEXT,                            
                                    skip_vectorization=True,
                                ),
                                wvc.config.Property(
                                    name="batch_id",
                                    data_type=wvc.config.DataType.TEXT,                            
                                    skip_vectorization=True,
                                ),
                            ]
                        ),
                        wvc.config.Property(
                            name="step_2",
                            data_type=wvc.config.DataType.OBJECT,                            
                            skip_vectorization=True,
                            nested_properties=[
                                wvc.config.Property(
                                    name="batch",
                                    data_type=wvc.config.DataType.TEXT,                            
                                    skip_vectorization=True,
                                ),
                                wvc.config.Property(
                                    name="system_fingerprint",
                                    data_type=wvc.config.DataType.TEXT,                            
                                    skip_vectorization=True,
                                ),
                                wvc.config.Property(
                                    name="batch_id",
                                    data_type=wvc.config.DataType.TEXT,                            
                                    skip_vectorization=True,
                                ),
                            ]
                        ), 
                    ]
                 ), 
                 wvc.config.Property(
                    name="uniqueId",
                    data_type=wvc.config.DataType.TEXT,                    
                    description= "",
                    skip_vectorization=True,
                 ),                  
            ]
        },
        {
            "class": "Chunk",
            "description": "Submission Chunks",
            "vectorizer_config": wvc.config.Configure.Vectorizer.none(),
            "properties": [  
                wvc.config.Property(
                    name="support",
                    data_type=wvc.config.DataType.TEXT,                    
                    skip_vectorization=True,
                ),                                                  
                wvc.config.Property(
                    name="regulation_type",
                    data_type=wvc.config.DataType.TEXT,                    
                    skip_vectorization=True,
                ),                
                wvc.config.Property(
                    name="regulator_trust",
                    data_type=wvc.config.DataType.TEXT,                
                    skip_vectorization=True,
                ),                           
                wvc.config.Property(
                    data_type=wvc.config.DataType.TEXT,
                    name="submitter",                    
                    skip_vectorization=True,
                ),                       
                wvc.config.Property(
                    name="group",
                    data_type=wvc.config.DataType.TEXT,                    
                    skip_vectorization=True,
                ),               
                wvc.config.Property(
                    name="submission_uniqueId",
                    data_type=wvc.config.DataType.TEXT,                    
                    skip_vectorization=True,
                ),
                wvc.config.Property(
                    name="chunk_text",
                    data_type=wvc.config.DataType.TEXT,                    
                    skip_vectorization=True,
                ),
                wvc.config.Property(
                    name="chunk_index",
                    data_type=wvc.config.DataType.NUMBER,                    
                    skip_vectorization=True,
                ),
            ]
        },
    ]
}
